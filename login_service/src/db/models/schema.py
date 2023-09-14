from pydantic import BaseModel, field_validator
from typing import Optional
from time import time

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str
    password_hash: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
