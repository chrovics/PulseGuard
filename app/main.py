from fastapi.responses import FileResponse
from fastapi import HTTPException
from app.models.ping_log import PingLog
from app.schemas.ping_log import PingLogResponse

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORTUL NOU
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from app.core.database import get_db
from app.models.monitor import Monitor
from app.schemas.monitor import MonitorCreate, MonitorResponse

app = FastAPI(
    title="PulseGuard API", 
    description="Uptime & SSL Monitoring Microservice",
    version="1.0.0"
)

# --- CONFIGURARE CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cereri de la orice origine (ex: frontend-ul nostru local)
    allow_credentials=True,
    allow_methods=["*"],  # Permite toate metodele HTTP (GET, POST, OPTIONS etc.)
    allow_headers=["*"],  # Permite toate headerele
)
# -----------------------------------

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- RUTE PENTRU MONITOARE ---

@app.post("/monitors", response_model=MonitorResponse, status_code=201)
async def create_monitor(monitor: MonitorCreate, db: AsyncSession = Depends(get_db)):
    """
    Adaugă un nou site pentru a fi monitorizat.
    """
    new_monitor = Monitor(
        url=str(monitor.url),  # Convertim tipul HttpUrl în string pentru baza de date
        name=monitor.name,
        check_interval_seconds=monitor.check_interval_seconds,
        user_id=monitor.user_id
    )
    db.add(new_monitor)
    await db.commit()
    await db.refresh(new_monitor)
    return new_monitor

@app.get("/monitors", response_model=list[MonitorResponse])
async def get_monitors(db: AsyncSession = Depends(get_db)):
    """
    Returnează lista tuturor site-urilor monitorizate din DB.
    """
    result = await db.execute(select(Monitor))
    monitors = result.scalars().all()
    return monitors

@app.get("/monitors/{monitor_id}/history", response_model=list[PingLogResponse])
async def get_monitor_history(monitor_id: int, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """
    Returnează ultimele 'limit' verificări (ping-uri) pentru un anumit monitor, 
    ordonate de la cel mai recent la cel mai vechi. Ideal pentru grafice (Chart.js).
    """
    # Verificăm dacă monitorul există
    monitor_query = await db.execute(select(Monitor).where(Monitor.id == monitor_id))
    monitor = monitor_query.scalar_one_or_none()
    
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitorul nu a fost găsit.")

    # Extragem istoricul ordonat descrescător după timp
    result = await db.execute(
        select(PingLog)
        .where(PingLog.monitor_id == monitor_id)
        .order_by(PingLog.checked_at.desc())
        .limit(limit)
    )
    
    return result.scalars().all()

@app.delete("/monitors/{monitor_id}")
async def delete_monitor(monitor_id: int, db: AsyncSession = Depends(get_db)):
    # Căutăm site-ul în baza de date
    result = await db.execute(select(Monitor).where(Monitor.id == monitor_id))
    monitor = result.scalar_one_or_none()
    
    if not monitor:
        raise HTTPException(status_code=404, detail="Site-ul nu a fost găsit")
        
    # Ștergem site-ul (regula CASCADE va șterge automat și istoricul lui de ping-uri)
    await db.delete(monitor)
    await db.commit()
    
    return {"message": "Monitor șters cu succes"}

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")
