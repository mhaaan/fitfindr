from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import get_db
from models.user import User
from utils.password import hash_password, verify_password

from schemas.user import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])

@router.post('/create_user')
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # First check for existing user
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    # Otherwise create user
    hashed_password = hash_password(user_data.password)

    db_user = User(
        email = user_data.email,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        password_hash = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)


