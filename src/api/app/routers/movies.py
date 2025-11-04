from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.movie_service import MovieService
from ..schemas.movie import MovieList

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

# get all movies
@router.get("/", response_model=List[MovieList])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movies(skip=skip, limit=limit)

