from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class GymBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=300)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=50)
    post_code: str = Field(..., min_length=1, max_length=20)


class GymCreate(GymBase):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")


class GymResponse(GymBase):
    id: int
    latitude: float
    longitude: float
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True