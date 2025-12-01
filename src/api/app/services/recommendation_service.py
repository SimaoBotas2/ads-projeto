from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.movie_repository import MovieRepository
from ..repositories.recommendation_repository import RecommendationRepository
from ..schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from ..repositories.recommendation_repository import RecommendationRepository

class RecommendationService:
    """Service for Recommendation business logic"""
    
    def __init__(self, db: Session):
        self.recommendation_repository = RecommendationRepository(db)
        self.movie_repository = MovieRepository(db)

    def get_recommendations_by_genre(self, user_id: int):
        recommendations_genres = self.recommendation_repository.get_top_genres_by_user(user_id)
        recommended_movies = []
        for genre in recommendations_genres:
            movies_in_genre = self.movie_repository.get_top_movies_genre_rated(genre.genre_id)
            recommended_movies.extend(movies_in_genre)
        return recommended_movies
    