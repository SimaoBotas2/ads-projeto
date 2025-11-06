from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import movie_cast


class Cast(Base):
    __tablename__ = "cast"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    biography = Column(Text)
    birth_date = Column(Date)
    birth_place = Column(String(100))
    profile_path = Column(String(300))
    
    # Relationships
    movies = relationship("Movie", secondary=movie_cast, back_populates="cast_members")
