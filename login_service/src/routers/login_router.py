from fastapi import APIRouter, Form, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from src.db.connect_to_db import get_db
from src.db.upload_to_db import register_new_user
from sqlalchemy.orm import Session
from src.db.models.schema import UserCreate
from src.db.models.models import User as UserModel
from src.utils import encrypt, check_password
from src.jwt_token.jwt_bearer import JWTBearer

login_router = APIRouter(prefix='/login', tags=['login'])


class UserLogin(BaseModel):
    username: str
    password: str


@login_router.post("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...), db: Session = Depends(
    get_db)):
    hashed_password = encrypt(password)
    register_new_user(db, UserCreate(username=username, password_hash=hashed_password, email=email))
    return {"message": "success"}


@login_router.post("/logout")
async def logout(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    return {"message": "success"}


@login_router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(user_data.username, user_data.password, db)

    if isinstance(user, str):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = JWTBearer.signJWT(user.id, user.username)

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@login_router.get("/temp_jwt/{user_id}")
async def temp_jwt(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    access_token = JWTBearer.signJWT(user_id, user.username)
    return access_token


def authenticate_user(username: str, password: str, db):
    login_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not login_user:
        return "User not found"
    if not check_password(password, login_user.password):
        return "Wrong password"
    return login_user
