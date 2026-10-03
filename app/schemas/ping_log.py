from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PingLogResponse(BaseModel):
    id: int
    monitor_id: int
    status_code: Optional[int]
    response_time_ms: Optional[float]
    is_up: bool
    error_message: Optional[str]
    checked_at: datetime

    class Config:
        from_attributes = True
