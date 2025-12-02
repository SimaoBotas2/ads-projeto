from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class UserBase(BaseModel):
    username: str = Field(..., max_length=512)
    email: EmailStr
    name: Optional[str] = Field(None, max_length=512)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=512)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=512)
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[date] = None
    
    model_config = {"from_attributes": True}
