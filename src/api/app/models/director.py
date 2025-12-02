from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import director_movie


class Director(Base):
    __tablename__ = "director"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    nacionality = Column(String(512))
    
    # Relationships
    movies = relationship("Movie", secondary=director_movie, back_populates="directors")
