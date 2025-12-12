from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.dependencies import get_current_user
from typing import List


from ..services.recommendation_service import RecommendationService
from ..database import get_db
from ..schemas.movie import MovieResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    dependencies=[Depends(get_current_user)]


)

@router.get("/genre", response_model=List[MovieResponse])
def get_recommendations_by_genre(user_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.get_recommendations_by_genre(user_id)


@router.get("/director", response_model=List[MovieResponse])
def get_recommendations_by_director(user_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.get_recommendations_by_director(user_id)


@router.get("/cast", response_model=List[MovieResponse])
def get_recommendations_by_cast(user_id: int, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.get_recommendations_by_cast(user_id)