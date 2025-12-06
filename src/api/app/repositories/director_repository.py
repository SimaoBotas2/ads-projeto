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
        return self.db.query(Director).filter(Director.id == director_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Director]:
        """Get all directors with pagination"""
        return self.db.query(Director).offset(skip).limit(limit).all()
    
    def create(self, director: DirectorCreate) -> Director:
        """Create a new director"""
        db_director = Director(
            name=director.name,
            nationality=director.nationality
        )
        self.db.add(db_director)
        self.db.commit()
        self.db.refresh(db_director)
        return db_director
    
    def update(self, director_id: int, director_update: DirectorUpdate) -> Optional[Director]:
        """Update director"""
        db_director = self.get_by_id(director_id)
        if not db_director:
            return None
        
        update_data = director_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_director, key, value)
        
        self.db.commit()
        self.db.refresh(db_director)
        return db_director
    
    def delete(self, director_id: int) -> bool:
        """Delete director"""
        db_director = self.get_by_id(director_id)
        if not db_director:
            return False
        
        self.db.delete(db_director)
        self.db.commit()
        return True
