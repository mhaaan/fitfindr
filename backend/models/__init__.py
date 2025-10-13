from models.database import Base, engine, SessionLocal
from models.gym import Gym
from models.trainer_gym import TrainerGym
from models.trainer import Trainer
from models.user import User

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()