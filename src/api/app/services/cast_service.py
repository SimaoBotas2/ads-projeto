from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.cast_repository import CastRepository
from ..schemas.cast import (
    CastCreate, 
    CastUpdate, 
    CastResponse,
    MovieCastCreate, 
    MovieCastUpdate, 
    MovieCastResponse
)


class CastService:
    """Service for Cast business logic"""
    
    def __init__(self, db: Session):
        self.repository = CastRepository(db)
    
    # Cast Management Methods
    def get_all_cast(self, skip: int = 0, limit: int = 100) -> List[CastResponse]:
        """Get all cast members"""
        cast_list = self.repository.get_all(skip, limit)
        return [CastResponse.model_validate(c) for c in cast_list]
    
    def get_cast_by_id(self, cast_id: int) -> Optional[CastResponse]:
        """Get cast member by ID"""
        cast = self.repository.get_by_id(cast_id)
        if cast:
            return CastResponse.model_validate(cast)
        return None
    
    def create_cast(self, cast: CastCreate) -> CastResponse:
        """Create new cast member"""
        new_cast = self.repository.create(cast)
        return CastResponse.model_validate(new_cast)
    
    def update_cast(self, cast_id: int, cast_update: CastUpdate) -> Optional[CastResponse]:
        """Update cast member"""
        updated_cast = self.repository.update(cast_id, cast_update)
        if updated_cast:
            return CastResponse.model_validate(updated_cast)
        return None
    
    def delete_cast(self, cast_id: int) -> bool:
        """Delete cast member"""
        return self.repository.delete(cast_id)
    
    # Movie-Cast Association Methods
    def get_cast_by_movie(self, movie_id: int) -> List[MovieCastResponse]:
        """Get all cast members for a movie"""
        cast_list = self.repository.get_cast_by_movie(movie_id)
        return [MovieCastResponse(**dict(cast)) for cast in cast_list]
    
    def get_movies_by_cast(self, cast_id: int) -> List[MovieCastResponse]:
        """Get all movies for a cast member"""
        movies_list = self.repository.get_movies_by_cast(cast_id)
        return [MovieCastResponse(**dict(movie)) for movie in movies_list]
    
    def add_cast_to_movie(self, movie_cast_data: MovieCastCreate) -> Optional[MovieCastResponse]:
        """Add cast member to movie"""
        result = self.repository.add_cast_to_movie(movie_cast_data)
        if result:
            return MovieCastResponse(**dict(result))
        return None
    
    def update_character_name(
        self, 
        movie_id: int, 
        cast_id: int, 
        character_name: str
    ) -> bool:
        """Update character name for a movie-cast relation"""
        return self.repository.update_character_name(movie_id, cast_id, character_name)
    
    def remove_cast_from_movie(self, movie_id: int, cast_id: int) -> bool:
        """Remove cast member from movie"""
        return self.repository.remove_cast_from_movie(movie_id, cast_id)
