from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import movie_director


class Director(Base):
    __tablename__ = "directors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    biography = Column(Text)
    birth_date = Column(Date)
    birth_place = Column(String(100))
    profile_path = Column(String(300))
    
    # Relationships
    movies = relationship("Movie", secondary=movie_director, back_populates="directors")
