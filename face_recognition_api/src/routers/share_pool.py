from fastapi import APIRouter, UploadFile, File, Form, Depends
from src.database.connect_to_db import get_db
from sqlalchemy.orm import Session, aliased
from src.flows.add_face import add_face
from sqlalchemy import func, and_
from src.flows.recognize import FaceRecognition
from src.jwt_handler import decode_jwt_token
from src.flows.add_face import add_face
from src.database.upload_to_db import upload_path_to_db, register_in_history, register_shared_image_pool, \
    register_user_in_sip, add_face_to_sip
from src.database.models.schema import Image, ImageCreate, User, RecognitionHistory, SharedImagePool, \
    SharedImagePoolFaces, SharedImagePoolMembers, SharedImagePoolPermissions
from src.database.models.models import SharedImagePool as SharedImagePoolModel
from src.database.models.models import SharedImagePoolMembers as SharedImagePoolMembersModel
from src.database.models.models import SharedImagePoolPermissions as SharedImagePoolPermissionsModel
from src.database.models.models import Image as ImageModel
from src.cloud_bucket.bucket_actions import BucketActions
from time import time

shared_image_pool_router = APIRouter(prefix='/shared_image_pool', tags=['shared_image_pool'])


@shared_image_pool_router.post("/create_group")
async def create_group(group_name: str = Form(...), token_payload: dict = Depends(decode_jwt_token),
                       db: Session = Depends(get_db)):
    _shared_image_pool = SharedImagePool(owner_id=token_payload['user_id'], image_pool_name=group_name)
    register_shared_image_pool(db=db, item=_shared_image_pool)


@shared_image_pool_router.post("/add_user_to_group")
async def add_user_to_group(group_name: str = Form(...), user_id: int = Form(...),
                            token_payload: dict = Depends(decode_jwt_token),
                            db: Session = Depends(get_db)):
    if token_payload['user_id'] != db.query(SharedImagePoolModel).filter(
            SharedImagePoolModel.image_pool_name == group_name).first().owner_id:
        return {"message": "You are not the owner of this group"}
    shared_pool_id = db.query(SharedImagePoolModel).filter(
        SharedImagePoolModel.image_pool_name == group_name).first().id
    register_user_in_sip(db=db, shared_pool_id=shared_pool_id, user_id=user_id)
    return {"message": "success"}


@shared_image_pool_router.post("/add_permissions_to_group")
async def add_permissions_to_group(group_name: str = Form(...), user_id: int = Form(...),
                                   read: bool = Form(...), write: bool = Form(...), delete: bool = Form(...),
                                   token_payload: dict = Depends(decode_jwt_token),
                                   db: Session = Depends(get_db)):
    if token_payload['user_id'] != db.query(SharedImagePoolModel).filter(
            SharedImagePoolModel.image_pool_name == group_name).first().owner_id:
        return {"message": "You are not the owner of this group"}
    shared_pool_id = db.query(SharedImagePoolModel).filter(
        SharedImagePoolModel.image_pool_name == group_name).first().id
    permissions = SharedImagePoolPermissionsModel(image_pool_id=shared_pool_id, user_id=user_id, read=read, write=write,
                                                  delete=delete)
    db.add(permissions)
    db.commit()
    db.refresh(permissions)
    return {"message": "success"}


@shared_image_pool_router.get("/get_all_sip_for_user")
def get_all_sip_for_user(token_payload: dict = Depends(decode_jwt_token),
                         db: Session = Depends(get_db)):
    # TODO: Make the output more readable
    user_id = token_payload['user_id']
    list_of_sips_owned_by_user = db.query(SharedImagePoolModel).filter(SharedImagePoolModel.owner_id == user_id).all()
    list_of_sips_shared_with_user = db.query(SharedImagePoolMembersModel).filter(
        SharedImagePoolMembersModel.user_id == user_id).all()

    concatened_list = []
    for item in list_of_sips_owned_by_user:
        concatened_list.append({"id": item.id, "owner": True})

    for item in list_of_sips_shared_with_user:
        concatened_list.append({"id": item.image_pool_id, "owner": False})
    return concatened_list


@shared_image_pool_router.post("/add_face_to_group")
async def add_face_to_group(group_name: str = Form(...), face_name: str = Form(...),
                            token_payload: dict = Depends(decode_jwt_token),
                            db: Session = Depends(get_db)):
    user_permissions = await get_permissions(db, group_name, token_payload)
    if not check_for_user_permissions(user_permissions):
        return {"message": "You don't have permissions to add faces to this group only to view"}

    subquery = (
        db.query(ImageModel.name, func.min(ImageModel.id).label("min_id"))
        .filter(ImageModel.user_id == token_payload["user_id"])
        .filter(ImageModel.name == face_name)
        .group_by(ImageModel.name)
        .subquery()
    )

    alias = aliased(ImageModel, name="im")

    image = (
        db.query(alias)
        .join(subquery, and_(alias.name == subquery.c.name, alias.id == subquery.c.min_id))
        .first()
    )
    image_pool_id = db.query(SharedImagePoolModel).filter(SharedImagePoolModel.image_pool_name == group_name).first().id
    add_face_to_sip(db, image, image_pool_id)
    image_folder = image.path.split('/')[0] + '/' + image.path.split('/')[1] + '/' + image.path.split('/')[2] + '/'

    BucketActions.copy_within_bucket(source_folder=image_folder,
                                     destination_folder=f'shared_pool_images/{image_pool_id}/{face_name}')

    return {"message": "success"}


async def get_permissions(db, group_name, token_payload):
    permissions_query = db.query(SharedImagePoolPermissionsModel).filter(
        SharedImagePoolPermissionsModel.user_id == token_payload['user_id']).filter(
        SharedImagePoolPermissionsModel.image_pool_id == db.query(SharedImagePoolModel).filter(
            SharedImagePoolModel.image_pool_name == group_name).first().id).first()
    if permissions_query is None:
        return SharedImagePoolPermissions(image_pool_id=0, user_id=0, read=False, write=False, delete=False)
    user_permissions = SharedImagePoolPermissions(image_pool_id=permissions_query.image_pool_id,
                                                  user_id=permissions_query.user_id,
                                                  read=permissions_query.read, write=permissions_query.write,
                                                  delete=permissions_query.delete)
    return user_permissions


def check_for_user_permissions(user_permissions: SharedImagePoolPermissions):
    if user_permissions.write:
        return True
    return False
