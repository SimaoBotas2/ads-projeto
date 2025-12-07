from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.movie_repository import MovieRepository
from ..schemas.rating import RatingCreate, RatingUpdate, RatingResponse

class RecommendationService:
    """Service for Recommendation business logic"""
    
    def __init__(self, db: Session):
        self.movie_repository = MovieRepository(db)

    def get_recommendations_by_genre(self, user_id: int):
        # Use a single SQLAlchemy query that computes genre averages and
        # returns movies ordered by genre average then movie average.
        return self.movie_repository.get_top_movies_for_user_genres(user_id)


