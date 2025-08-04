from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class InteractionType(str, enum.Enum):
    will_watch = "will_watch"
    already_watched = "already_watched"
    not_for_me = "not_for_me"

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='user_movie_unique'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    interaction_type = Column(Enum(InteractionType))

    # Optional: for easy relationship navigation
    user = relationship("User", back_populates="interactions")
    movie = relationship("Movie")
