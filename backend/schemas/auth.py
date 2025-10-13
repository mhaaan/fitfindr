from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """TODO."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password (min 8 characters)")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str