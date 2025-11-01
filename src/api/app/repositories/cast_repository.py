from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.cast import Cast
from ..schemas.cast import CastCreate, CastUpdate


class CastRepository:
    """Repository for Cast database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, cast_id: int) -> Optional[Cast]:
        """Get cast member by ID"""
        # TODO: Implement
        pass
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cast]:
        """Get all cast members with pagination"""
        # TODO: Implement
        pass
    
    def create(self, cast: CastCreate) -> Cast:
        """Create a new cast member"""
        # TODO: Implement
        pass
    
    def update(self, cast_id: int, cast_update: CastUpdate) -> Optional[Cast]:
        """Update cast member"""
        # TODO: Implement
        pass
    
    def delete(self, cast_id: int) -> bool:
        """Delete cast member"""
        # TODO: Implement
        pass
