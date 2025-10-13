from fastapi import APIRouter, Depends, HTTPException, status
from geoalchemy2.functions import ST_Point, ST_X, ST_Y, ST_DWithin
from geoalchemy2.types import Geography
from sqlalchemy import cast
from sqlalchemy.orm import Session

from models import get_db
from models.gym import Gym
from models.trainer import Trainer
from models.trainer_gym import TrainerGym
from schemas.trainer import TrainerResponse
from utils.password import hash_password, verify_password
from utils.utils import map_object_to_model

from schemas.gym import GymCreate, GymResponse

router = APIRouter(prefix="/gyms", tags=["gyms"])

@router.post('/create_gym')
def create_gym(gym_data: GymCreate, db: Session = Depends(get_db)):
    # From the gym location model, we retrieve the latitude and longitude
    # Right now user would need to put long/lat themselves
    # NOTE: Find a way for address to long/lat conversion
    lat, long = (gym_data.latitude, gym_data.longitude)
    location_point = ST_Point(lat, long)

    existing_gym = db.query(Gym).filter(Gym.location == location_point).first()
    if existing_gym:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Gym already exists'
        )
    
    db_gym = Gym(
        name=gym_data.name,
        address=gym_data.address,
        city=gym_data.city,
        state=gym_data.state,
        post_code=gym_data.post_code,
        location=location_point
    )
    db.add(db_gym)
    db.commit()
    db.refresh(db_gym)


@router.get('/get_gym/{gym_id}')
def get_gym(gym_id: int, db: Session=Depends(get_db)) -> GymResponse:
    result = db.query(
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
    ).filter(Gym.id == gym_id).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Gym does not exist'
        )

    gym_response = GymResponse(
        id=result.id,
        name=result.name,
        address=result.address,
        city=result.city,
        state=result.state,
        post_code=result.post_code,
        longitude=result.longitude,
        latitude=result.latitude,
        created_at=result.created_at,
        is_active=result.is_active
    )
    return gym_response


@router.get('/get_all_gyms')
def get_all_gyms(db: Session = Depends(get_db)) -> list[GymResponse]:
    gym_data = []
    results = db.query(
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
    ).all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No gyms to show'
        )

    for result in results:
        gym_response = GymResponse(
            id=result.id,
            name=result.name,
            address=result.address,
            city=result.city,
            state=result.state,
            post_code=result.post_code,
            longitude=result.longitude,
            latitude=result.latitude,
            created_at=result.created_at,
            is_active=result.is_active
        )
        gym_data.append(gym_response)
    
    return gym_data


@router.get('get_nearby_gyms/{radius}')
def get_nearby_gyms(latitude: float, longitude: float, radius: int, db: Session = Depends(get_db)):
    gym_data = []
    location_point = ST_Point(latitude, longitude)
    
    results = db.query(
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
    ).filter(
        ST_DWithin(
            cast(location_point, Geography),
            cast(Gym.location, Geography),
            radius * 1000
        )
    ).all()

    print(results)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No gyms to show'
        )

    for result in results:
        gym_response = GymResponse(
            id=result.id,
            name=result.name,
            address=result.address,
            city=result.city,
            state=result.state,
            post_code=result.post_code,
            longitude=result.longitude,
            latitude=result.latitude,
            created_at=result.created_at,
            is_active=result.is_active
        )
        gym_data.append(gym_response)
    
    return gym_data


@router.get('/{gym_id}/gyms')
def get_all_trainers_for_gym(gym_id: int, db: Session = Depends(get_db)) -> list[TrainerResponse]:
    trainers = []
    result = db.query(Trainer
        ).join(TrainerGym, TrainerGym.trainer_id == Trainer.id
        ).filter(TrainerGym.gym_id == gym_id
        ).filter(TrainerGym.is_active == True
        ).all()

    for trainer in result:
        working_trainer = TrainerResponse(
            email=trainer.email,
            first_name=trainer.first_name,
            last_name=trainer.last_name,
            bio=trainer.bio,
            specializations=trainer.specializations,
            certifications=trainer.certifications,
            hourly_rate=trainer.hourly_rate,
            years_experince=trainer.years_experience,
            id=trainer.id,
            created_at=trainer.created_at,
            is_active=trainer.is_active,
            is_available=trainer.is_available
        )
        trainers.append(working_trainer)
    
    return trainers


# 51.54715610181569, -0.0073675846528802776