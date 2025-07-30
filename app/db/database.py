from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine with SSL for Supabase
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # Required for Supabase
)

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()
