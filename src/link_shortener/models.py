from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timedelta
from src.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String(100), unique=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expire_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=1))
    is_active = Column(Boolean, default=True)
    redirect_count = Column(Integer, default=0)
