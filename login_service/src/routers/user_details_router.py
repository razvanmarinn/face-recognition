from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.connect_to_db import get_db
from src.db.models.schema import UserDetailsCreate
from src.db.models.models import User
from src.db.upload_to_db import get_user_details, edit_user_details

user_details_routers = APIRouter(prefix='/user_details', tags=['user_details'])


@user_details_routers.post("/edit_user_details")
async def edit_user_detail(user_id: int, user_details: UserDetailsCreate, db: Session = Depends(
    get_db)):
    return edit_user_details(db, user_id=user_id, user_details=user_details)


@user_details_routers.get("/get_user_details")
async def get_user_detail(user_id: int, db: Session = Depends(
    get_db)):
    return get_user_details(db, user_id=user_id)


@user_details_routers.get("/get_user_id")
async def get_user_id(username: str, db: Session = Depends(
    get_db)):
    return db.query(User).filter(User.username == username).first().id

@user_details_routers.get("/get_number_of_total_users")
async def get_number_of_total_users(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    return {"total_users": total_users}