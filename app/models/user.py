from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    dob = Column(Date, nullable=False)
    pincode = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    has_completed_onboarding = Column(Boolean, default=False)
    preferred_genres = Column(JSONB, nullable=True)         # comma-separated genre IDs
    preferred_languages = Column(JSONB, nullable=True)      # comma-separated language codes
    preferred_mood = Column(JSONB, nullable=True)


    interactions = relationship("UserInteraction", back_populates="user")
