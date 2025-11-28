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
        return self.db.query(Genre).filter(Genre.id == genre_id).first()
    
    def get_all(self) -> List[Genre]:
        """Get all genres"""
        return self.db.query(Genre).all()
    
    def create(self, genre: GenreCreate) -> Genre:
        """Create a new genre"""
        db_genre = Genre(
            name=genre.name,
            description=genre.description
        )
        self.db.add(db_genre)
        self.db.commit()
        self.db.refresh(db_genre)
        return db_genre
    
    def update(self, genre_id: int, genre_update: GenreUpdate) -> Optional[Genre]:
        """Update genre"""
        db_genre = self.get_by_id(genre_id)
        if not db_genre:
            return None
        
        update_data = genre_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_genre, key, value)
        
        self.db.commit()
        self.db.refresh(db_genre)
        return db_genre
    
    def delete(self, genre_id: int) -> bool:
        """Delete genre"""
        db_genre = self.get_by_id(genre_id)
        if not db_genre:
            return False
        
        self.db.delete(db_genre)
        self.db.commit()
        return True
