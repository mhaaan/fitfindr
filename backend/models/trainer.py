from models.database import Base

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Numeric

class Trainer(Base):
    __tablename__ = 'trainers'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    bio = Column(Text)
    specializations = Column(String(500))
    certifications = Column(String(300))
    hourly_rate = Column(Numeric(5, 2))
    years_experience = Column(Integer)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)