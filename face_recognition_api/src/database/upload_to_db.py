from sqlalchemy.orm import Session
from src.database.models import models, schema
from src.database.models.schema import Image, ImageCreate, UserCreate, RecognitionHistory, SharedImagePool, \
    SharedImagePoolFaces, SharedImagePoolMembers, SharedImagePoolPermissions


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def upload_path_to_db(db: Session, item: Image):
    db_item = models.Image(name=item.name, path=item.path, size=item.size, user_id=item.user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def register_in_history(db: Session, item: schema.RecognitionHistory):
    db_item = models.RecognitionHistory(path=item.path, user_id=item.user_id, face_name=item.face_name,
                                        timestamp=item.timestamp, success_status=item.success_status)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def register_shared_image_pool(db: Session, item: schema.SharedImagePool):
    db_item = models.SharedImagePool(owner_id=item.owner_id, image_pool_name=item.image_pool_name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def register_user_in_sip(db: Session, shared_pool_id: int, user_id: int):
    db_item = models.SharedImagePoolMembers(image_pool_id=shared_pool_id, user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
