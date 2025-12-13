from sqlalchemy.orm import Session
from typing import List
from ..repositories.genre_repository import GenreRepository
from ..schemas.genre import GenreResponse


class GenreService:
    def __init__(self, db: Session):
        self.repository = GenreRepository(db)

    def get_all_genres(self) -> List[GenreResponse]:
        genres = self.repository.get_all()
        return [GenreResponse.model_validate(genre) for genre in genres]

    def get_genre_by_id(self, genre_id: int) -> GenreResponse | None:
        genre = self.repository.get_by_id(genre_id)
        if genre:
            return GenreResponse.model_validate(genre)
        return None
