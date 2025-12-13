from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.genre import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Genre]:
        return self.db.query(Genre).order_by(Genre.name).all()

    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.id == genre_id).first()

    def get_by_name(self, name: str) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.name == name).first()
