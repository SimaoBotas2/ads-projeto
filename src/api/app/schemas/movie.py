from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class MovieBase(BaseModel):
    name: str = Field(..., max_length=524)
    launch_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=512)
    nationality: Optional[str] = Field(None, max_length=512)
    poster_path: Optional[str] = Field(None, max_length=512)


class MovieCreate(MovieBase):
    genre_ids: Optional[List[int]] = []
    director_ids: Optional[List[int]] = []
    cast_ids: Optional[List[int]] = []


class MovieUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=524)
    launch_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=512)
    nationality: Optional[str] = Field(None, max_length=512)
    poster_path: Optional[str] = Field(None, max_length=512)
    genre_ids: Optional[List[int]] = None
    director_ids: Optional[List[int]] = None
    cast_ids: Optional[List[int]] = None


class GenreResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class DirectorResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CastResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class MovieResponse(MovieBase):
    id: int
    genres: List[GenreResponse] = []
    directors: List[DirectorResponse] = []
    cast_members: List[CastResponse] = []
    average_rating: Optional[float] = None
    count_rating: int = 0

    model_config = {"from_attributes": True}


class MovieList(BaseModel):
    id: int
    name: str
    launch_date: Optional[date] = None
    poster_path: Optional[str] = None
    
    model_config = {"from_attributes": True}


class RecommendedMovieResponse(BaseModel):
    """Schema for recommended movies with name and genres"""
    id: int
    name: str
    genres: List[GenreResponse] = []
    
    model_config = {"from_attributes": True}
