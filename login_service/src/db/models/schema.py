from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    password_hash: str


class UserCreate(UserBase):
    email: str
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserDetailsBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str

    class Config:
        orm_mode = True


class UserDetailsCreate(UserDetailsBase):
    pass
