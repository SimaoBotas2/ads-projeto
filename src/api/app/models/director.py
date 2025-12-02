from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import director_movie


class Director(Base):
    __tablename__ = "director"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, nullable=False)
    nationality = Column(String(512))
    
    # Relationships
    movies = relationship("Movie", secondary=director_movie, back_populates="directors")
