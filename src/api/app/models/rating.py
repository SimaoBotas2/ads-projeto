from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, event
from sqlalchemy.orm import relationship, Session
from ..database import Base


class Rating(Base):
    __tablename__ = "rating"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evaluation = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('_user_.id', ondelete='CASCADE'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    
    __table_args__ = (
        CheckConstraint('evaluation > 0 AND evaluation < 5', name='evaluation'),
    )
