from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import movie_cast


class Cast(Base):
    __tablename__ = "cast"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    nacionality = Column(String(512))
    
    # Relationships
    movies = relationship("Movie", secondary=movie_cast, back_populates="cast_members")
