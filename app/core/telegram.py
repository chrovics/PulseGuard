import os
import httpx
from dotenv import load_dotenv

# Încărcăm în memorie variabilele ascunse din fișierul .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_alert(message: str):
    """Trimite un mesaj text către botul tău de Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Token-ul sau Chat ID-ul lipsesc din .env!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML" # Permite folosirea tag-urilor <b> pentru bold
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=5.0)
            response.raise_for_status()
            print("📩 Alertă trimisă cu succes pe Telegram!")
        except Exception as e:
            print(f"❌ Eroare la trimiterea alertei: {e}")
