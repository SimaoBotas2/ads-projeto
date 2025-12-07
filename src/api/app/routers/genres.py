from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services.genre_service import GenreService
from ..schemas.genre import GenreCreate, GenreUpdate, GenreResponse
from ..utils.dependencies import get_current_user

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[GenreResponse])
def get_all_genres(db: Session = Depends(get_db)):
    service = GenreService(db)
    return service.get_all_genres()


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    service = GenreService(db)
    result = service.get_genre_by_id(genre_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return result


@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    service = GenreService(db)
    return service.create_genre(genre)


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(genre_id: int, genre_update: GenreUpdate, db: Session = Depends(get_db)):
    service = GenreService(db)
    updated = service.update_genre(genre_id, genre_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return updated


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    service = GenreService(db)
    deleted = service.delete_genre(genre_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return None
