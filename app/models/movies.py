from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Date
from app.db.database import Base
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Local ID
    tmdb_id = Column(Integer, nullable=False, unique=True)  # TMDB Movie ID

    title = Column(String, nullable=False)
    original_title = Column(String)
    original_language = Column(String)
    overview = Column(Text)
    release_date = Column(Date)  # ✅ Proper Date column
    popularity = Column(Float)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    poster_path = Column(String)
    backdrop_path = Column(String)
    video = Column(Boolean)

    # Relationship to main movie table
    features = relationship("MovieFeature", back_populates="movie", uselist=False)
