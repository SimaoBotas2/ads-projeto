from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.director import Director
from ..schemas.director import DirectorCreate, DirectorUpdate


class DirectorRepository:
    """Repository for Director database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, director_id: int) -> Optional[Director]:
        """Get director by ID"""
        # TODO: Implement
        pass
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Director]:
        """Get all directors with pagination"""
        # TODO: Implement
        pass
    
    def create(self, director: DirectorCreate) -> Director:
        """Create a new director"""
        # TODO: Implement
        pass
    
    def update(self, director_id: int, director_update: DirectorUpdate) -> Optional[Director]:
        """Update director"""
        # TODO: Implement
        pass
    
    def delete(self, director_id: int) -> bool:
        """Delete director"""
        # TODO: Implement
        pass
