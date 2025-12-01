from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.api.app.services.recommendation_service import RecommendationService
from ..database import get_db
from ..services.rating_service import RatingService
from ..schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from ..repositories.rating_repository import RatingRepository

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.get("/genre", response_model=List[RatingResponse])
def get_recommendations_by_genre(user_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.get_recommendations_by_genre(user_id)