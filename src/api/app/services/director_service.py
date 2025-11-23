from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.director_repository import DirectorRepository
from ..schemas.director import DirectorCreate, DirectorUpdate, DirectorResponse


class DirectorService:
    """Service for Director business logic"""
    
    def __init__(self, db: Session):
        self.repository = DirectorRepository(db)
    
    def get_all_directors(self, skip: int = 0, limit: int = 100) -> List[DirectorResponse]:
        """Get all directors"""
        directors = self.repository.get_all(skip, limit)
        return [DirectorResponse.model_validate(d) for d in directors]
    
    def get_director_by_id(self, director_id: int) -> Optional[DirectorResponse]:
        """Get director by ID"""
        director = self.repository.get_by_id(director_id)
        if director:
            return DirectorResponse.model_validate(director)
        return None
    
    def create_director(self, director: DirectorCreate) -> DirectorResponse:
        """Create new director"""
        new_director = self.repository.create(director)
        return DirectorResponse.model_validate(new_director)
    
    def update_director(self, director_id: int, director_update: DirectorUpdate) -> Optional[DirectorResponse]:
        """Update director"""
        updated_director = self.repository.update(director_id, director_update)
        if updated_director:
            return DirectorResponse.model_validate(updated_director)
        return None
    
    def delete_director(self, director_id: int) -> bool:
        """Delete director"""
        return self.repository.delete(director_id)
