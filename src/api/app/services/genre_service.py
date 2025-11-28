from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.genre_repository import GenreRepository
from ..schemas.genre import GenreCreate, GenreUpdate, GenreResponse


class GenreService:
    """Service for Genre business logic"""
    
    def __init__(self, db: Session):
        self.repository = GenreRepository(db)
    
    def get_all_genres(self) -> List[GenreResponse]:
        """Get all genres"""
        genres = self.repository.get_all()
        return [GenreResponse.model_validate(g) for g in genres]
    
    def get_genre_by_id(self, genre_id: int) -> Optional[GenreResponse]:
        """Get genre by ID"""
        genre = self.repository.get_by_id(genre_id)
        if genre:
            return GenreResponse.model_validate(genre)
        return None
    
    def create_genre(self, genre: GenreCreate) -> GenreResponse:
        """Create new genre"""
        new_genre = self.repository.create(genre)
        return GenreResponse.model_validate(new_genre)
    
    def update_genre(self, genre_id: int, genre_update: GenreUpdate) -> Optional[GenreResponse]:
        """Update genre"""
        updated_genre = self.repository.update(genre_id, genre_update)
        if updated_genre:
            return GenreResponse.model_validate(updated_genre)
        return None
    
    def delete_genre(self, genre_id: int) -> bool:
        """Delete genre"""
        return self.repository.delete(genre_id)
