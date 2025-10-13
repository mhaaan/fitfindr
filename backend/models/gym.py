from models.database import Base

from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey

class Gym(Base):
    __tablename__ = 'gyms'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    post_code = Column(String(20), nullable=False)
    location = Column(Geometry('POINT'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)