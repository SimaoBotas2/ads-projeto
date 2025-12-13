from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.genre_service import GenreService
from ..schemas.genre import GenreResponse
from ..utils.dependencies import get_current_user

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[GenreResponse])
def get_genres(db: Session = Depends(get_db)):
    service = GenreService(db)
    return service.get_all_genres()


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    service = GenreService(db)
    genre = service.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre
