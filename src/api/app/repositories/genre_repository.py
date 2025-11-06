from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.genre import Genre
from ..schemas.genre import GenreCreate, GenreUpdate


class GenreRepository:
    """Repository for Genre database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        """Get genre by ID"""
        # TODO: Implement
        pass
    
    def get_all(self) -> List[Genre]:
        """Get all genres"""
        # TODO: Implement
        pass
    
    def create(self, genre: GenreCreate) -> Genre:
        """Create a new genre"""
        # TODO: Implement
        pass
    
    def update(self, genre_id: int, genre_update: GenreUpdate) -> Optional[Genre]:
        """Update genre"""
        # TODO: Implement
        pass
    
    def delete(self, genre_id: int) -> bool:
        """Delete genre"""
        # TODO: Implement
        pass
