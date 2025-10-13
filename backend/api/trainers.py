from fastapi import APIRouter, Depends, HTTPException, status
from geoalchemy2.functions import ST_Point, ST_X, ST_Y, ST_DWithin
from geoalchemy2.types import Geography
from sqlalchemy import cast
from sqlalchemy.orm import Session

from models import get_db
from models.trainer import Trainer
from utils.password import hash_password, verify_password
from utils.utils import map_object_to_model

from schemas.trainer import TrainerCreate, TrainerResponse

router = APIRouter(prefix="/trainers", tags=["trainers"])

@router.post('/create_trainer')
def create_trainer(trainer_data: TrainerCreate, db: Session = Depends(get_db)):
    # First check for existing trainer
    existing_trainer = db.query(Trainer).filter(Trainer.email == trainer_data.email).first()
    if existing_trainer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered'
        )
    # Otherwise create user
    hashed_password = hash_password(trainer_data.password)

    db_trainer = Trainer(
        email = trainer_data.email,
        first_name = trainer_data.first_name,
        last_name = trainer_data.last_name,
        password_hash = hashed_password,
        bio = trainer_data.bio,
        specializations = trainer_data.specializations,
        certifications = trainer_data.certifications,
        hourly_rate = trainer_data.hourly_rate,
        years_experience = trainer_data.years_experience
    )

    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
