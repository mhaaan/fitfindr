from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional

# TrainerBase - shared fields (email, name, bio, professional info)
# TrainerCreate - for registration (includes password, certifications, specializations, rates)
# TrainerResponse - for API output (no password, includes id and timestamps)

class TrainerBase(BaseModel):
    email: EmailStr = Field(..., description="Trainer's email address")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    specializations: Optional[str] = Field(None, max_length=500)
    certifications: Optional[str] = Field(None, max_length=300)
    hourly_rate: Optional[float] = Field(None, gt=0)
    years_experience: Optional[int] = Field(None, ge=0)

class TrainerCreate(TrainerBase):
    password: str = Field(..., min_length=8, max_length=100)

class TrainerResponse(TrainerBase):
    id: int
    created_at: datetime
    is_active: bool
    is_available: bool  # Not