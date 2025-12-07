from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.rating_repository import RatingRepository
from ..schemas.rating import RatingCreate, RatingUpdate, RatingResponse


class RatingService:
    """Service for Rating business logic"""
    
    def __init__(self, db: Session):
        self.repository = RatingRepository(db)
    
    def get_user_ratings(self, user_id: int) -> List[RatingResponse]:
        """Get all ratings by user"""
        ratings = self.repository.get_by_user(user_id)
        return [RatingResponse.model_validate(r) for r in ratings]

    def get_movie_ratings(self, movie_id: int) -> List[RatingResponse]:
        """Get all ratings for a movie"""
        ratings = self.repository.get_by_movie(movie_id)
        return [RatingResponse.model_validate(r) for r in ratings]

    def create_rating(self, rating: RatingCreate, user_id: int) -> RatingResponse:
        """Create or update rating"""
        existing = self.repository.get_user_movie_rating(user_id, rating.movie_id)
        if existing:
            updated = self.repository.update(existing.id, rating)
            return RatingResponse.model_validate(updated)
        new_rating = self.repository.create(rating, user_id)
        return RatingResponse.model_validate(new_rating)

    def update_rating(self, rating_id: int, rating_update: RatingUpdate, user_id: int) -> Optional[RatingResponse]:
        """Update rating (only if owned by user)"""
        existing = self.repository.get_by_id(rating_id)
        if not existing or existing.user_id != user_id:
            return None
        updated = self.repository.update(rating_id, rating_update)
        return RatingResponse.model_validate(updated) if updated else None

    def get_user_rating_for_movie(self, user_id: int, movie_id: int):
        return self.repository.get_user_movie_rating(user_id, movie_id)


    def delete_rating(self, rating_id: int, user_id: int) -> bool:
        """Delete rating (only if owned by user)"""
        existing = self.repository.get_by_id(rating_id)
        if not existing or existing.user_id != user_id:
            return False
        return self.repository.delete(rating_id)
