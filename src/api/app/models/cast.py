from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import movie_cast


class Cast(Base):
    __tablename__ = "cast"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(512), nullable=False)
    nacionality = Column(String(512))
    
    # Relationships
    movies = relationship("Movie", secondary=movie_cast, back_populates="cast_members")
