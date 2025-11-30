from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.movie import Movie
from ..schemas.movie import MovieCreate, MovieUpdate
from ..models.genre import Genre


class MovieRepository:
    """Repository for Movie database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie by ID with all relationships eager-loaded"""
        return (
            self.db.query(Movie)
            .options(
                joinedload(Movie.genres),
                joinedload(Movie.directors),
                joinedload(Movie.cast_members),
                joinedload(Movie.ratings)
            )
            .filter(Movie.id == movie_id)
            .first()
        )
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        """Get all movies with pagination"""
        return self.db.query(Movie).offset(skip).limit(limit).all()
    
    def search(self, query: str) -> List[Movie]:
        """Search movies by name or keyword"""
        return self.db.query(Movie).filter(Movie.name.ilike(f"%{query}%")).all()
    
    def get_by_genre(self, genre_id: int) -> List[Movie]:
        """Get movies by genre"""
        return self.db.query(Movie).join(Movie.genres).filter(Genre.id == genre_id).all()
    
    def get_recommended(self, limit: int = 10) -> List[Movie]:
        """Get recommended movies - simple implementation returns recent movies"""
        return (
            self.db.query(Movie)
            .filter(Movie.launch_date.isnot(None))
            .order_by(Movie.launch_date.desc())
            .limit(limit)
            .all()
        )
    
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
