from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.movie_service import MovieService
from ..schemas.movie import MovieList, MovieResponse

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

# get movie by id
@router.get("/{movie_id}", response_model=MovieList)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movie(movie_id)

# get all movies
@router.get("/", response_model=List[MovieList])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movies(skip=skip, limit=limit)

# search movies by title or keyword
@router.get("/search/", response_model=List[MovieList])
def search_movies(query: str, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.search_movies(query)

# get movies by genre
@router.get("/genre/{genre_id}", response_model=List[MovieList])
def get_movies_by_genre(genre_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movies_by_genre(genre_id)
