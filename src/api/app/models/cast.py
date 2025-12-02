from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from ..database import Base
from .movie import movie_cast


class Cast(Base):
    __tablename__ = "cast"
    
<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    biography = Column(Text)
    birth_date = Column(Date)
    birth_place = Column(String(100))
=======
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(512), nullable=False)
    nacionality = Column(String(512))
>>>>>>> 849c1700b1ccc3b55e958f00191b9456900e4c56
    
    # Relationships
    movies = relationship("Movie", secondary=movie_cast, back_populates="cast_members")
