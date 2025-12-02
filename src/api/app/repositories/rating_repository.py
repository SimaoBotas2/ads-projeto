from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.rating import Rating
from ..schemas.rating import RatingCreate, RatingUpdate
from .movie_repository import MovieRepository


class RatingRepository:
    """Repository for Rating database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, rating_id: int) -> Optional[Rating]:
        """Get rating by ID"""
        return self.db.query(Rating).filter(Rating.id == rating_id).first()
    
    def get_by_user(self, user_id: int) -> List[Rating]:
        """Get all ratings by user"""
        return self.db.query(Rating).filter(Rating.user_id == user_id).all()
    
    def get_by_movie(self, movie_id: int) -> List[Rating]:
        """Get all ratings for a movie"""
        return self.db.query(Rating).filter(Rating.movie_id == movie_id).all()
    
    def get_user_movie_rating(self, user_id: int, movie_id: int) -> Optional[Rating]:
        """Get specific user rating for a movie"""
        return (
            self.db.query(Rating)
            .filter(Rating.user_id == user_id, Rating.movie_id == movie_id)
            .first()
        )
    
    def create(self, rating: RatingCreate, user_id: int) -> Rating:
        """Create a new rating"""
        new_rating = Rating(
            user_id=user_id,
            movie_id=rating.movie_id,
            evaluation=rating.evaluation,
        )
        self.db.add(new_rating)
        self.db.commit()
        self.db.refresh(new_rating)
        # Update aggregates using MovieRepository helper (atomic, optimized)
        try:
            MovieRepository(self.db).increment_rating(new_rating.movie_id, new_rating.rating)
        except Exception:
            try:
                MovieRepository(self.db).recalculate_rating(new_rating.movie_id)
            except Exception:
                pass
        return new_rating
    
    def update(self, rating_id: int, rating_update: RatingUpdate) -> Optional[Rating]:
        """Update rating"""
        db_rating = self.get_by_id(rating_id)
        if not db_rating:
            return None
        update_data = rating_update.model_dump(exclude_unset=True)
        old_rating_value = db_rating.rating
        for key, value in update_data.items():
            setattr(db_rating, key, value)
        self.db.commit()
        self.db.refresh(db_rating)
        # Update aggregatings using MovieRepository helper (atomic, optimized)
        try:
            MovieRepository(self.db).adjust_rating_on_update(db_rating.movie_id, old_rating_value, db_rating.rating)
        except Exception:
            try:
                MovieRepository(self.db).recalculate_rating(db_rating.movie_id)
            except Exception:
                pass
        return db_rating
    
    def delete(self, rating_id: int) -> bool:
        """Delete rating"""
        db_rating = self.get_by_id(rating_id)
        if not db_rating:
            return False
        movie_id = db_rating.movie_id
        rating_value = db_rating.rating
        self.db.delete(db_rating)
        self.db.commit()
        # Update aggregatings using MovieRepository helper (atomic, optimized)
        try:
            MovieRepository(self.db).decrement_rating(movie_id, rating_value)
        except Exception:
            try:
                MovieRepository(self.db).recalculate_rating(movie_id)
            except Exception:
                pass
        return True
