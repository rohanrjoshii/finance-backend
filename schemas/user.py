from pydantic import BaseModel, EmailStr
from typing import Optional
from models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdateRole(BaseModel):
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str
