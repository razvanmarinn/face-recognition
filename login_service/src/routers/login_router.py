
from fastapi import APIRouter, UploadFile, File, Form, Depends
from src.database.connect_to_db import get_db
from src.database.upload_to_db import register_new_user
from sqlalchemy.orm import Session
from src.database.models.schema import UserCreate, User
from src.database.models.models import User as UserModel
from src.utils import encrypt, check_password

login_router = APIRouter(prefix='/login', tags=['login'])


@login_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    login_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not login_user:
        return "User not found"
    if not check_password(password, login_user.password):
        return "Wrong password"

    return "success"


@login_router.post("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...), db: Session = Depends(
    get_db)):
    hashed_password = encrypt(password)
    register_new_user(db, UserCreate(username=username, password_hash=hashed_password, email=email))
    return {"message": "success"}


@login_router.post("/logout")
async def logout(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    return {"message": "success"}
