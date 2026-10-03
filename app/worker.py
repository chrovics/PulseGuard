import asyncio
from datetime import datetime, timezone
from sqlalchemy.future import select

from app.core.database import AsyncSessionLocal
from app.models.monitor import Monitor
from app.models.ping_log import PingLog
from app.services.checker import check_http_status
from app.services.ssl_checker import get_ssl_expiry
from app.core.telegram import send_telegram_alert  # <-- IMPORTUL NOU (Curierul nostru)

async def check_monitors():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Încep verificarea monitoarelor...")
    
    async with AsyncSessionLocal() as db:
        # 1. Extragem doar site-urile active
        result = await db.execute(select(Monitor).where(Monitor.is_active == True))
        monitors = result.scalars().all()

        if not monitors:
            print("Nu există monitoare active în baza de date.")
            return

        for monitor in monitors:
            print(f" -> Testez: {monitor.url}")
            
            # 2. Executăm testele de rețea
            http_res = await check_http_status(monitor.url)
            ssl_res = get_ssl_expiry(monitor.url)
            
            # --- 🚨 LOGICA DE ALERTARE TELEGRAM (State Transition) ---
            is_currently_up = http_res["is_up"]
            
            # Dacă înainte era UP și acum e DOWN -> Alertă de picare
            if monitor.is_up is True and is_currently_up is False:
                mesaj = f"🔴 <b>ALERTĂ DOWN</b>\nSite: {monitor.url}\nEroare: HTTP {http_res.get('status_code')} / {http_res.get('error_message')}"
                await send_telegram_alert(mesaj)
            
            # Dacă înainte era DOWN și acum e UP -> Alertă de recuperare
            elif monitor.is_up is False and is_currently_up is True:
                mesaj = f"🟢 <b>RECOVERY</b>\nSite: {monitor.url}\nServiciul și-a revenit! Latență: {http_res['response_time_ms']} ms"
                await send_telegram_alert(mesaj)
            # ---------------------------------------------------------
            
            # 3. Creăm o intrare nouă în tabelul de istoric
            ping_log = PingLog(
                monitor_id=monitor.id,
                status_code=http_res["status_code"],
                response_time_ms=http_res["response_time_ms"],
                is_up=http_res["is_up"],
                error_message=http_res["error_message"]
            )
            db.add(ping_log)
            
            # 4. Actualizăm starea curentă în tabelul principal
            monitor.is_up = is_currently_up
            monitor.last_status_code = http_res["status_code"]
            monitor.last_response_time_ms = http_res["response_time_ms"]
            monitor.last_checked_at = datetime.now(timezone.utc)
            
            if ssl_res["valid"]:
                monitor.ssl_valid_until = datetime.fromisoformat(ssl_res["expires_at"])
                monitor.ssl_issuer = ssl_res["issuer"]
            
        # 5. Salvăm totul deodată în PostgreSQL
        await db.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Verificare completă și salvată cu succes!")

async def main():
    print("🚀 PulseGuard Worker pornit. Aștept să execut verificările...")
    while True:
        await check_monitors()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
