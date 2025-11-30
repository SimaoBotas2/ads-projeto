from pydantic import BaseModel, Field
from typing import Optional


class DirectorBase(BaseModel):
    name: str
    nacionality: Optional[str] = Field(None, max_length=512)


class DirectorCreate(DirectorBase):
    pass


class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    nacionality: Optional[str] = Field(None, max_length=512)


class DirectorResponse(DirectorBase):
    id: int
    
    model_config = {"from_attributes": True}
