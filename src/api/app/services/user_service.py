from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserUpdate
from ..models.user import User
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    # No password hashing
    def hash_password(self, password: str) -> str:
        return password

    def verify_password(self, plain_password: str, stored_password: str) -> bool:
        return plain_password == stored_password

    def create_user(self, user_create: UserCreate) -> User:
        # store password as-is
        return self.repo.create(user_create, user_create.password)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repo.get_by_username(username)

    def update_user(self, user: User, updates: UserUpdate) -> User:
        if updates.password:
            updates.password = updates.password  # no hashing
        return self.repo.update(user, updates)

    def delete_user(self, user: User) -> None:
        self.repo.delete(user)
