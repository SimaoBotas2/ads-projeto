import hashlib, os
from datetime import date
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserUpdate
from ..models.user import User
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)  # 16-byte random salt
        salt_hex = salt.hex()
        hash_hex = hashlib.sha256(salt + password.encode()).hexdigest()
        return f"{salt_hex}:{hash_hex}"

    def verify_password(self, plain_password: str, stored: str) -> bool:
        salt_hex, hash_hex = stored.split(":")
        salt = bytes.fromhex(salt_hex)
        calc = hashlib.sha256(salt + plain_password.encode()).hexdigest()
        return calc == hash_hex

    def create_user(self, user_create: UserCreate) -> User:
        hashed = self.hash_password(user_create.password)
        return self.repo.create(user_create, hashed)

    def update_user(self, user: User, updates: UserUpdate) -> User:
        if updates.password:
            updates.password = self.hash_password(updates.password)
        return self.repo.update(user, updates)
    
    def update_last_login(self, user: User) -> None:
        """Update the user's last login timestamp"""
        user.last_login = date.today()
        self.repo.db.commit()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repo.get_by_username(username)

    def delete_user(self, user: User) -> None:
        self.repo.delete(user)
