from models.database import Base

from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean

class TrainerGym(Base):
    __tablename__ = 'trainer_gyms'
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)
    gym_id = Column(Integer, ForeignKey('gyms.id'), nullable=False)
    started_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)