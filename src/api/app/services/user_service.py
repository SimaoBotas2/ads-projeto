from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserUpdate
from ..models.user import User
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.hash_password(user_create.password)
        return self.repo.create(user_create, hashed_password)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repo.get_by_username(username)

    def update_user(self, user: User, updates: UserUpdate) -> User:
        if updates.password:
            updates.password = self.hash_password(updates.password)
        return self.repo.update(user, updates)

    def delete_user(self, user: User) -> None:
        self.repo.delete(user)
