from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.rating_service import RatingService
from ..schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from ..utils.dependencies import get_current_user

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/user/{user_id}", response_model=List[RatingResponse])
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    service = RatingService(db)
    return service.get_user_ratings(user_id)


@router.get("/movie/{movie_id}", response_model=List[RatingResponse])
def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    service = RatingService(db)
    return service.get_movie_ratings(movie_id)


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
def create_rating(rating: RatingCreate, user_id: int, db: Session = Depends(get_db)):
    service = RatingService(db)
    return service.create_rating(rating, user_id)


@router.put("/", response_model=RatingResponse)
def update_rating(
    rating_id: int,
    rating_update: RatingUpdate,
    user_id: int,
    db: Session = Depends(get_db),
):
    service = RatingService(db)
    updated = service.update_rating(rating_id, rating_update, user_id)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or unauthorized"
        )
    return updated


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int, user_id: int, db: Session = Depends(get_db)):
    service = RatingService(db)
    deleted = service.delete_rating(rating_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or unauthorized"
        )
    return None

@router.get("/{movie_id}", response_model=RatingResponse)
def get_rating_for_user_and_movie(
    movie_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    service = RatingService(db)
    rating = service.get_user_rating_for_movie(user_id, movie_id)

    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found for this user/movie"
        )

    return rating
