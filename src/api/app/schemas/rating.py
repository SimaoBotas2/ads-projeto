from pydantic import BaseModel, Field
from typing import Optional


class RatingBase(BaseModel):
    movie_id: int
    evaluation: int = Field(..., gt=0, lt=5)  # Must be between 1 and 4


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    evaluation: Optional[int] = Field(None, gt=0, lt=5)


class RatingResponse(RatingBase):
    id: int
    user_id: int
    
    model_config = {"from_attributes": True}
