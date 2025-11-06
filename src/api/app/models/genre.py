from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import movie_genre


class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(500))
    
    # Relationships
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")
