from sqlalchemy.orm import Session
from typing import List, Optional, Any
from ..models.cast import Cast
from ..models.movie import movie_cast, Movie
from ..schemas.cast import CastCreate, CastUpdate


class CastRepository:
    """Repository for Cast database operations and movie-cast associations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # --- CRUD Methods ---
    def get_by_id(self, cast_id: int) -> Optional[Cast]:
        """Get cast member by ID"""
        return self.db.query(Cast).filter(Cast.id == cast_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cast]:
        """Get all cast members with pagination"""
        return self.db.query(Cast).offset(skip).limit(limit).all()
    
    def create(self, cast: CastCreate) -> Cast:
        """Create a new cast member"""
        db_cast = Cast(
            name=cast.name,
            nacionality=cast.nacionality
        )
        self.db.add(db_cast)
        self.db.commit()
        self.db.refresh(db_cast)
        return db_cast
    
    def update(self, cast_id: int, cast_update: CastUpdate) -> Optional[Cast]:
        """Update cast member"""
        db_cast = self.get_by_id(cast_id)
        if not db_cast:
            return None
        
        update_data = cast_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cast, key, value)
        
        self.db.commit()
        self.db.refresh(db_cast)
        return db_cast
    
    def delete(self, cast_id: int) -> bool:
        """Delete cast member"""
        db_cast = self.get_by_id(cast_id)
        if not db_cast:
            return False
        
        self.db.delete(db_cast)
        self.db.commit()
        return True
    
    # --- Movie-Cast Association Methods ---
    def get_cast_by_movie(self, movie_id: int) -> List[Any]:
        """Get all cast members for a movie"""
        return (
            self.db.query(movie_cast)
            .filter(movie_cast.c.movie_id == movie_id)
            .all()
        )
    
    def get_movies_by_cast(self, cast_id: int) -> List[Any]:
        """Get all movies for a cast member"""
        return (
            self.db.query(movie_cast)
            .filter(movie_cast.c.cast_id == cast_id)
            .all()
        )
    
    def get_movie_cast_relation(self, movie_id: int, cast_id: int) -> Optional[Any]:
        """Get specific movie-cast relation"""
        return (
            self.db.query(movie_cast)
            .filter(
                movie_cast.c.movie_id == movie_id,
                movie_cast.c.cast_id == cast_id
            )
            .first()
        )
    
    def add_cast_to_movie(self, movie_cast_data: Any) -> Optional[Any]:
        """Add cast member to movie"""
        # Check if movie exists
        movie = self.db.query(Movie).filter(Movie.id == movie_cast_data.movie_id).first()
        if not movie:
            return None
        
        # Check if cast exists
        cast = self.get_by_id(movie_cast_data.cast_id)
        if not cast:
            return None
        
        # Check if relation already exists
        existing = self.get_movie_cast_relation(movie_cast_data.movie_id, movie_cast_data.cast_id)
        if existing:
            return None
        
        # Add new relation
        stmt = movie_cast.insert().values(
            movie_id=movie_cast_data.movie_id,
            cast_id=movie_cast_data.cast_id
        )
        self.db.execute(stmt)
        self.db.commit()
        
        return self.get_movie_cast_relation(movie_cast_data.movie_id, movie_cast_data.cast_id)
    
    def remove_cast_from_movie(self, movie_id: int, cast_id: int) -> bool:
        """Remove cast member from movie"""
        stmt = (
            movie_cast.delete()
            .where(
                movie_cast.c.movie_id == movie_id,
                movie_cast.c.cast_id == cast_id
            )
        )
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount > 0
