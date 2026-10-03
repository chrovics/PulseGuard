from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False) # Simplificat momentan
    url = Column(String(512), nullable=False)
    name = Column(String(100), nullable=False)
    check_interval_seconds = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    last_status_code = Column(Integer, nullable=True)
    last_response_time_ms = Column(Numeric(8, 2), nullable=True)
    is_up = Column(Boolean, default=True)
    ssl_valid_until = Column(DateTime(timezone=True), nullable=True)
    ssl_issuer = Column(String(255), nullable=True)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
