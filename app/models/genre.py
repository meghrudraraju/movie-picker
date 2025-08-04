from sqlalchemy import Column, Integer, String
from app.db.database import Base  # This is your declarative base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)  # TMDB genre ID
    name = Column(String, nullable=False, unique=True)
