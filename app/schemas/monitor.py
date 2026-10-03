from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# Schema pentru crearea unui monitor (ce primim la POST)
class MonitorCreate(BaseModel):
    url: HttpUrl
    name: str
    check_interval_seconds: int = 60
    user_id: int = 1 # Hardcodat momentan, până facem autentificarea

# Schema pentru returnarea unui monitor (ce trimitem la GET)
class MonitorResponse(BaseModel):
    id: int
    user_id: int
    url: HttpUrl
    name: str
    check_interval_seconds: int
    is_active: bool
    is_up: bool
    last_status_code: Optional[int] = None
    last_response_time_ms: Optional[float] = None
    ssl_valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True
