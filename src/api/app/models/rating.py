from sqlalchemy import Column, BigInteger, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base


class Rating(Base):
    __tablename__ = "rating"
    
    id = Column(BigInteger, primary_key=True, index=True)
    evaluation = Column(Integer, nullable=False)
    user_id = Column(BigInteger, ForeignKey('_user_.id', ondelete='CASCADE'), nullable=False)
    movie_id = Column(BigInteger, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    
    __table_args__ = (
        CheckConstraint('evaluation > 0 AND evaluation < 5', name='evaluation'),
    )
