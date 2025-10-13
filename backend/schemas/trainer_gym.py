from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional


class TrainerGymCreate(BaseModel):
    gym_id: int
    started_date: Optional[datetime]


class TrainerGymResponse(BaseModel):
    id: int
    trainer_id: int
    gym_id: int
    started_date: Optional[datetime]
    created_at: datetime
    is_active: bool