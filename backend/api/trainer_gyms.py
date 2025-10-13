from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from geoalchemy2.functions import ST_Point, ST_X, ST_Y, ST_DWithin
from geoalchemy2.types import Geography
from sqlalchemy import cast
from sqlalchemy.orm import Session

from models import get_db
from models.gym import Gym
from models.trainer import Trainer
from models.trainer_gym import TrainerGym
from schemas.gym import GymResponse
from utils.password import hash_password, verify_password
from utils.utils import map_object_to_model

from schemas.trainer import TrainerCreate, TrainerResponse
from schemas.trainer_gym import TrainerGymCreate, TrainerGymResponse

router = APIRouter(prefix="/trainer_gyms", tags=["trainer_gyms"])

@router.post('/{trainer_id}/gyms')
def add_gym_to_trainer(trainer_id: int, trainer_gym_data: TrainerGymCreate, db: Session = Depends(get_db)):
    existing_trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    if not existing_trainer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Trainer does not exist'
        )
    existing_gym = db.query(Gym).filter(Gym.id == trainer_gym_data.gym_id).first()
    if not existing_gym:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Gym does not exist'
        )
    
    existing_trainer_gym = db.query(TrainerGym).filter(
        TrainerGym.trainer_id == trainer_id,
        TrainerGym.gym_id == trainer_gym_data.gym_id,
    ).first()

    if existing_trainer_gym.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Trainer already works here'
        )
    else:
        existing_trainer_gym.is_active = True
        db.session.commit()

    if not existing_trainer_gym:
        new_gym = TrainerGym(
            trainer_id=trainer_id,
            gym_id=trainer_gym_data.gym_id,
            started_date=trainer_gym_data.started_date or datetime.now(),
            created_at=datetime.now(),
            is_active=True
        )
        db.add(new_gym)
        db.commit()
        db.refresh(new_gym)

    
@router.get('/{trainer_id}/gyms')
def get_all_trainer_gyms(trainer_id: int, db: Session = Depends(get_db)) -> list[GymResponse]:
    gym_locations = []
    gyms_for_trainer = db.query(
        Gym.id,
        Gym.name,
        Gym.address,
        Gym.city,
        Gym.state,
        Gym.post_code,
        ST_X(Gym.location).label('longitude'),
        ST_Y(Gym.location).label('latitude'),
        Gym.created_at,
        Gym.is_active
    ).join(TrainerGym, Gym.id == TrainerGym.gym_id
    ).filter(TrainerGym.trainer_id == trainer_id 
    ).filter(TrainerGym.is_active == True
    ).all()

    if not gyms_for_trainer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cant get gyms'
        )

    for gym in gyms_for_trainer:
        gym_response = GymResponse(
            id=gym.id,
            name=gym.name,
            address=gym.address,
            city=gym.city,
            state=gym.state,
            post_code=gym.post_code,
            longitude=gym.longitude,
            latitude=gym.latitude,
            created_at=gym.created_at,
            is_active=gym.is_active
        )
        gym_locations.append(gym_response)
    return gym_locations

    
    