from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..services.cast_service import CastService
from ..schemas.cast import (
    CastCreate, 
    CastUpdate, 
    CastResponse, 
    MovieCastCreate,
    MovieCastUpdate,
    CastWithCharacterResponse
)


router = APIRouter(
    prefix="/cast",
    tags=["cast"]
)


@router.get("/", response_model=List[CastResponse])
def get_all_cast(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CastService(db)
    return service.get_all_cast(skip=skip, limit=limit)


@router.get("/{cast_id}", response_model=CastResponse)
def get_cast(cast_id: int, db: Session = Depends(get_db)):
    service = CastService(db)
    result = service.get_cast_by_id(cast_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cast not found")
    return result


@router.post("/", response_model=CastResponse, status_code=status.HTTP_201_CREATED)
def create_cast(cast: CastCreate, db: Session = Depends(get_db)):
    service = CastService(db)
    return service.create_cast(cast)


@router.put("/{cast_id}", response_model=CastResponse)
def update_cast(cast_id: int, cast_update: CastUpdate, db: Session = Depends(get_db)):
    service = CastService(db)
    updated = service.update_cast(cast_id, cast_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cast not found")
    return updated


@router.delete("/{cast_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cast(cast_id: int, db: Session = Depends(get_db)):
    service = CastService(db)
    deleted = service.delete_cast(cast_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cast not found")
    return None


# --- Association endpoints (cast <-> movie) ---
@router.get("/{cast_id}/movies", response_model=List[dict])
def get_movies_by_cast(cast_id: int, db: Session = Depends(get_db)):
    service = CastService(db)
    return service.get_movies_by_cast(cast_id)


@router.post("/{cast_id}/movies", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_cast_to_movie(cast_id: int, payload: MovieCastCreate, db: Session = Depends(get_db)):
    service = CastService(db)
    # Create proper payload with cast_id included
    movie_cast_data = MovieCastCreate(
        movie_id=payload.movie_id, 
        cast_id=cast_id, 
        character_name=payload.character_name
    )
    result = service.add_cast_to_movie(movie_cast_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid movie_id, cast_id, or relation already exists")
    return result


@router.put("/{cast_id}/movies/{movie_id}", response_model=dict)
def update_character_name(cast_id: int, movie_id: int, payload: MovieCastUpdate, db: Session = Depends(get_db)):
    service = CastService(db)
    if payload.character_name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="character_name is required")
    updated = service.update_character_name(movie_id, cast_id, payload.character_name)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie-Cast relation not found")
    return {"message": "Character name updated successfully"}


@router.delete("/{cast_id}/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cast_from_movie(cast_id: int, movie_id: int, db: Session = Depends(get_db)):
    service = CastService(db)
    deleted = service.remove_cast_from_movie(movie_id, cast_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie-Cast relation not found")
    return None
