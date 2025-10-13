import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is our 'database connection manager'. Handles connecting to PostgresSQL
engine = create_engine(os.getenv('DATABASE_URL'), echo=True)

# This creates a 'factory' for our database session. Each time we need to talk to the db,a  new session is created.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)
# This is the parent cless for all our database tables. Provides all SQLAlchemy functionality
Base = declarative_base()

