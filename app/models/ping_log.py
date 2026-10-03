from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class PingLog(Base):
    __tablename__ = "ping_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    monitor_id = Column(Integer, ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Numeric(8, 2), nullable=True)
    is_up = Column(Boolean, nullable=False)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
