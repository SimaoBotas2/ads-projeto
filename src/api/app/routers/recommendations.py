from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..services.recommendation_service import RecommendationService
from ..database import get_db
from ..schemas.movie import MovieResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.get("/genre", response_model=List[MovieResponse])
def get_recommendations_by_genre(user_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.get_recommendations_by_genre(user_id)