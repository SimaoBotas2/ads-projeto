from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Float, nullable=False)  # e.g., 1.0 to 5.0 or 1.0 to 10.0
    review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    
    # Ensure one rating per user per movie
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),
    )
