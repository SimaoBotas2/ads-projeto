from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class MovieSimple(BaseModel):
    id: int
    name: str
    launch_date: Optional[date] = None
    poster_path: Optional[str] = None
    
    model_config = {"from_attributes": True}


class RatingBase(BaseModel):
    evaluation: int = Field(..., ge=1, le=5)  # Must be between 1 and 5


class RatingCreate(RatingBase):
    movie_id: int


class RatingUpdate(BaseModel):
    evaluation: Optional[int] = Field(None, ge=1, le=5)


class RatingResponse(RatingBase):
    id: int
    user_id: int
    movie: MovieSimple
    
    model_config = {"from_attributes": True}
