from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import genre_movie


class Genre(Base):
    __tablename__ = "genre"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(512), unique=True, nullable=False)
    
    # Relationships
    movies = relationship("Movie", secondary=genre_movie, back_populates="genres")
