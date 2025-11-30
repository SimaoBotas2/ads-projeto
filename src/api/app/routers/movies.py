from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.movie_service import MovieService
from ..services.cast_service import CastService
from ..schemas.movie import MovieList, MovieResponse, RecommendedMovieResponse
from ..schemas.cast import CastWithCharacterResponse

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

# get all movies
@router.get("/", response_model=List[MovieList])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movies(skip=skip, limit=limit)

# search movies by name or keyword
@router.get("/search/", response_model=List[MovieList])
def search_movies(query: str, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.search_movies(query)

# get movies by genre
@router.get("/genre/{genre_id}", response_model=List[MovieList])
def get_movies_by_genre(genre_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_movies_by_genre(genre_id)

""" # get recommended movies
@router.get("/recommendations/top", response_model=List[RecommendedMovieResponse])
def get_recommended_movies(limit: int = 10, db: Session = Depends(get_db)):
    service = MovieService(db)
    return service.get_recommended_movies(limit=min(limit, 10)) """

# get movie by id
@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService(db)
    movie = service.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

""" # get cast members for a movie
@router.get("/{movie_id}/cast", response_model=List[CastWithCharacterResponse])
def get_movie_cast(movie_id: int, db: Session = Depends(get_db)):
    service = CastService(db)
    return service.get_cast_by_movie(movie_id) """
