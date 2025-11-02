from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from typing import Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: User, updates: UserUpdate) -> User:
        for field, value in updates.dict(exclude_unset=True).items():
            if field == "password":
                continue
            setattr(db_user, field, value)
        if updates.password:
            db_user.hashed_password = updates.password  # hashed by service
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, db_user: User) -> None:
        self.db.delete(db_user)
        self.db.commit()
