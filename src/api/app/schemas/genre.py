from pydantic import BaseModel, Field
from typing import Optional


class GenreBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=500)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)


class GenreResponse(GenreBase):
    id: int
    
    model_config = {"from_attributes": True}
