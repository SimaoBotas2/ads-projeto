from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.movie import Movie
from ..schemas.movie import MovieCreate, MovieUpdate


class MovieRepository:
    """Repository for Movie database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie by ID"""
        # TODO: Implement
        pass
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Get all movies with pagination"""
        # TODO: Implement
        pass
    
    def search(self, query: str) -> List[Movie]:
        """Search movies by title"""
        # TODO: Implement
        pass
    
    def get_by_genre(self, genre_id: int) -> List[Movie]:
        """Get movies by genre"""
        # TODO: Implement
        pass
    
    def create(self, movie: MovieCreate) -> Movie:
        """Create a new movie"""
        # TODO: Implement
        pass
    
    def update(self, movie_id: int, movie_update: MovieUpdate) -> Optional[Movie]:
        """Update movie"""
        # TODO: Implement
        pass
    
    def delete(self, movie_id: int) -> bool:
        """Delete movie"""
        # TODO: Implement
        pass
