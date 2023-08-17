from sqlalchemy.orm import Session
from src.database.models import models, schema
from src.database.models.schema import Image, ImageCreate


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def upload_path_to_db(db: Session, item: Image):
    db_item = models.Image(id = 0, name = item.name, path = item.path, size = item.size, user_id = item.user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
