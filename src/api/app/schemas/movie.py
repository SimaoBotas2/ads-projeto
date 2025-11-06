from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class MovieBase(BaseModel):
    title: str = Field(..., max_length=200)
    original_title: Optional[str] = Field(None, max_length=200)
    overview: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=300)
    release_date: Optional[date] = None
    runtime: Optional[int] = Field(None, gt=0)
    budget: Optional[int] = Field(None, ge=0)
    revenue: Optional[int] = Field(None, ge=0)
    poster_path: Optional[str] = Field(None, max_length=300)
    backdrop_path: Optional[str] = Field(None, max_length=300)
    imdb_id: Optional[str] = Field(None, max_length=20)
    original_language: Optional[str] = Field(None, max_length=10)
    popularity: Optional[float] = Field(None, ge=0)
    vote_average: Optional[float] = Field(None, ge=0, le=10)
    vote_count: Optional[int] = Field(None, ge=0)


class MovieCreate(MovieBase):
    genre_ids: Optional[List[int]] = []
    director_ids: Optional[List[int]] = []
    cast_ids: Optional[List[int]] = []


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    original_title: Optional[str] = Field(None, max_length=200)
    overview: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=300)
    release_date: Optional[date] = None
    runtime: Optional[int] = Field(None, gt=0)
    budget: Optional[int] = Field(None, ge=0)
    revenue: Optional[int] = Field(None, ge=0)
    poster_path: Optional[str] = Field(None, max_length=300)
    backdrop_path: Optional[str] = Field(None, max_length=300)
    imdb_id: Optional[str] = Field(None, max_length=20)
    original_language: Optional[str] = Field(None, max_length=10)
    popularity: Optional[float] = Field(None, ge=0)
    vote_average: Optional[float] = Field(None, ge=0, le=10)
    vote_count: Optional[int] = Field(None, ge=0)
    genre_ids: Optional[List[int]] = None
    director_ids: Optional[List[int]] = None
    cast_ids: Optional[List[int]] = None


class MovieResponse(MovieBase):
    id: int
    
    model_config = {"from_attributes": True}


class MovieList(BaseModel):
    id: int
    title: str
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    vote_average: Optional[float] = None
    
    model_config = {"from_attributes": True}
