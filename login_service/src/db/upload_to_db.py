from sqlalchemy.orm import Session
from src.db.models import models, schema


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def register_new_user(db: Session, user: schema.UserCreate):
    db_user = models.User(username=user.username, password=user.password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user_details = models.UserDetails(user_id=db_user.id, email=user.email)
    db.add(db_user_details)
    db.commit()
    return db_user


def get_user_details(db: Session, user_id: int):
    return db.query(models.UserDetails).filter(models.UserDetails.user_id == user_id).first()


def edit_user_details(db: Session, user_id: int, user_details: schema.UserDetailsCreate):
    db_user_details = get_user_details(db, user_id=user_id)

    if db_user_details:
        db_user_details.first_name = user_details.first_name
        db_user_details.last_name = user_details.last_name
        db_user_details.age = user_details.age
        db_user_details.email = user_details.email
    else:
        db_user_details = models.UserDetails(user_id=user_id,
                                             first_name=user_details.first_name,
                                             last_name=user_details.last_name,
                                             age=user_details.age,
                                             email=user_details.email)
        db.add(db_user_details)

    db.commit()
    db.refresh(db_user_details)
    return db_user_details
