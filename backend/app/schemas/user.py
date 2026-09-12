"""
Pydantic schemas (request/response contracts) for authentication and user data.
Keeping schemas separate from DB models keeps API contracts explicit and safe
(e.g. password_hash is never returned to the client).
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    preferred_language: str = Field(default="en", pattern="^(en|hi|mr)$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    preferred_language: str
    training_score: int
    virtual_balance: float
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
