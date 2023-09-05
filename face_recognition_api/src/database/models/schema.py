from pydantic import BaseModel, field_validator
from typing import Optional
from time import time


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


class ImageCreate(BaseModel):
    name: str
    path: Optional[str] = None
    user_id: int

    def __init__(self, **data):
        super().__init__(**data)
        if self.path is None:
            self.path = self.generate_path()
    def generate_path(self):
        timestamp = time()
        return f"faces/{self.user_id}/{self.name}/{self.name}_{timestamp}.jpg"


class Image(ImageCreate):
    size: int

    @field_validator('size')
    def size_must_be_positive(cls, v):
        assert v > 0, 'size must be positive'
        return v


    class Config:
        orm_mode = True


class RecognitionHistory(BaseModel):
    path: str
    user_id: int
    face_name: str
    timestamp: float
    success_status: bool

    class Config:
        orm_mode = True