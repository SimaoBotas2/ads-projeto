from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserRepository:
    """Repository for User database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        # TODO: Implement
        pass
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        # TODO: Implement
        pass
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        # TODO: Implement
        pass
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        # TODO: Implement
        pass
    
    def create(self, user: UserCreate) -> User:
        """Create a new user"""
        # TODO: Implement
        pass
    
    def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        # TODO: Implement
        pass
    
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        # TODO: Implement
        pass
