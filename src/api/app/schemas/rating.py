from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RatingBase(BaseModel):
    movie_id: int
    rating: float = Field(..., ge=0, le=10)
    review: Optional[str] = None


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0, le=10)
    review: Optional[str] = None


class RatingResponse(RatingBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}
