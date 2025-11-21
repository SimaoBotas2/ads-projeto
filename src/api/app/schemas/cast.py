from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CastBase(BaseModel):
    name: str = Field(..., max_length=100)
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = Field(None, max_length=100)
    profile_path: Optional[str] = Field(None, max_length=300)


class CastCreate(CastBase):
    pass


class CastUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = Field(None, max_length=100)
    profile_path: Optional[str] = Field(None, max_length=300)


class CastResponse(CastBase):
    id: int
    
    model_config = {"from_attributes": True}


# --- Movie-Cast Association Schemas ---
class MovieCastBase(BaseModel):
    movie_id: int
    cast_id: int
    character_name: Optional[str] = None


class MovieCastCreate(MovieCastBase):
    pass


class MovieCastUpdate(BaseModel):
    character_name: Optional[str] = None


class MovieCastResponse(MovieCastBase):
    model_config = {"from_attributes": True}


class MovieCastDetailResponse(BaseModel):
    movie_id: int
    cast_id: int
    character_name: Optional[str] = None
    cast_member: CastResponse
    
    model_config = {"from_attributes": True}
