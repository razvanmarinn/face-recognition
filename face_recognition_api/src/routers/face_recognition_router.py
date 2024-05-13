from fastapi import APIRouter, UploadFile, File, Form, Depends
from src.database.connect_to_db import get_db
from sqlalchemy.orm import Session
from src.flows.recognize import FaceRecognition
from src.jwt_handler import decode_jwt_token
from src.flows.add_face import add_face
from src.database.upload_to_db import upload_path_to_db, register_in_history
from src.database.models.schema import Image, ImageCreate, User, RecognitionHistory
from src.routers.share_pool import get_all_sip_for_user
from time import time
from src.kafka.KafkaHandler import KafkaHandler
from typing import List, Optional
from src.cloud_bucket.bucket_actions import BucketActions


recognition_router = APIRouter(prefix='/face_recognition', tags=['face_recognition'])
face_recognition = FaceRecognition()


@recognition_router.post("/add_face")
async def face_recognition_add_face(name: str = Form("Default"), image: UploadFile = File(...),
                                    token_payload: dict = Depends(decode_jwt_token),
                                    db: Session = Depends(get_db),
                                    face_auth: bool = Form(False)):
    try:
        image_content = await image.read()
        file_size = len(image_content)
        image = Image(name=name, size=file_size, user_id=token_payload['user_id'])
        if face_auth:
            # image.name = get_user_name(token_payload['user_id'], db) # TODO: to add user details and implement this
            timestamp = time()
            image.path = f"faces/{image.user_id}/face_auth/{image.name}_{timestamp}.jpg"
        add_face(image.path, image_content)
        upload_path_to_db(db=db, item=image)
        return {"message": "success"}
    except Exception as e:
        return {"message": e, "status": "failed"}


@recognition_router.post("/recognize")
async def recognize(
        face_name: Optional[str] = Form(None),
        image: UploadFile = File(...),
        token_payload: dict = Depends(decode_jwt_token),
        db: Session = Depends(get_db),
        default_face_auth: bool = Form(False)
):
    try:
        user_id = token_payload['user_id']
        username = token_payload['username']
        timestamp = time()
        image_content = await image.read()
        file_size = len(image_content)
        user = User(id=user_id, username=username)
        image = Image(name="temp", size=file_size, user_id=user.id)
        list_of_ids = [item['id'] for item in get_all_sip_for_user(token_payload=token_payload, db=db)]

        if default_face_auth:
            face_recognition.encode_faces_for_face_auth(user=user)
        elif len(list_of_ids) > 0 and not default_face_auth:
            face_recognition.encode_faces(user=user, face_name=face_name, pool_mode=True,
                                          pool_list=list_of_ids)
        else:
            face_recognition.encode_faces(user, face_name)

        result = face_recognition.recognize(image_content)
        status = result[0]['details']['name'] == face_name or result[0]['details']['name'] == 'unknown'

        register_in_history(
            db, item=RecognitionHistory(
                path=image.path,
                user_id=user.id,
                face_name=face_name,
                timestamp=timestamp,
                success_status=status
            )
        )

        return result

    except Exception as e:
        return {"message": str(e), "status": "failed"}


@recognition_router.post("/face_auth_recognize")
async def face_auth_recognize(
        user_id: int = Form(...),
        list_of_images: List[UploadFile] = File(...),
):
    try:
        kafka_handler = KafkaHandler("test2", "face_auth_response")
        # Send images using the existing KafkaHandler instance
        await kafka_handler.send_images_to_kafka(list_of_images, user_id)

        return {"message": "Recognition process initiated", "status_endpoint": "/check_recognition_status"}
    except Exception as e:
        return {"message": str(e), "status": "failed"}


@recognition_router.get("/check_recognition_status/{user_id}")
async def check_recognition_status(user_id: int):
    try:
        kafka_handler = KafkaHandler("test2", "face_auth_response")
        recognized = await kafka_handler.wait_for_recognition(user_id)

        if recognized:
            return {"message": "Recognition successful", "status": "success"}
        else:
            return {"message": "Recognition in progress or failed", "status": "in_progress_or_failed"}
    except Exception as e:
        return {"message": str(e), "status": "failed"}


@recognition_router.get("/get_faces/{face_name}")
async def get_faces(face_name: str, token_payload: dict = Depends(decode_jwt_token), db: Session = Depends(get_db)):
    user_id = token_payload['user_id']
    link_of_images = BucketActions.retrieve_all_image_urls(user_id, face_name)
    return link_of_images

