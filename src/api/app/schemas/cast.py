from pydantic import BaseModel, Field
from typing import Optional


class CastBase(BaseModel):
    name: str = Field(..., max_length=512)
    nacionality: Optional[str] = Field(None, max_length=512)


class CastCreate(CastBase):
    pass


class CastUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=512)
    nacionality: Optional[str] = Field(None, max_length=512)


class CastResponse(CastBase):
    id: int
    
    model_config = {"from_attributes": True}


# --- Movie-Cast Association Schemas ---
class MovieCastBase(BaseModel):
    movie_id: int
    cast_id: int


class MovieCastCreate(MovieCastBase):
    pass


class CastWithCharacterResponse(BaseModel):
    """Cast member for a specific movie"""
    id: int
    name: str
    nacionality: Optional[str] = None
    
    model_config = {"from_attributes": True}


class MovieCastDetailResponse(BaseModel):
    movie_id: int
    cast_id: int
    cast_member: CastResponse
    model_config = {"from_attributes": True}

