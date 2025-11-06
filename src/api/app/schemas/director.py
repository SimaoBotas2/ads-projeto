from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class DirectorBase(BaseModel):
    name: str = Field(..., max_length=100)
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = Field(None, max_length=100)
    profile_path: Optional[str] = Field(None, max_length=300)


class DirectorCreate(DirectorBase):
    pass


class DirectorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = Field(None, max_length=100)
    profile_path: Optional[str] = Field(None, max_length=300)


class DirectorResponse(DirectorBase):
    id: int
    
    model_config = {"from_attributes": True}
