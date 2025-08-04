from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class MovieFeature(Base):
    __tablename__ = "movie_features"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tmdb_id = Column(Integer, ForeignKey("movies.tmdb_id"), unique=True, nullable=False)

    feature_string = Column(Text)
    vector = Column(Text)  # Optional: store JSON string or comma-separated floats

    # Establishes a link back to the Movie model
    movie = relationship("Movie", back_populates="features")
