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

recognition_router = APIRouter(prefix='/face_recognition', tags=['face_recognition'])
face_recognition = FaceRecognition()


@recognition_router.post("/add_face")
async def face_recognition_add_face(name: str = Form(...), image: UploadFile = File(...),
                                    token_payload: dict = Depends(decode_jwt_token),
                                    db: Session = Depends(get_db)):
    try:
        image_content = await image.read()
        file_size = len(image_content)
        image = Image(name=name, size=file_size, user_id=token_payload['user_id'])
        add_face(image.path, image_content)
        upload_path_to_db(db=db, item=image)
        return {"message": "success"}
    except Exception as e:
        return {"message": e, "status": "failed"}


@recognition_router.post("/recognize")
async def recognize(
        face_name: str = Form(...),
        image: UploadFile = File(...),
        token_payload: dict = Depends(decode_jwt_token),
        db: Session = Depends(get_db)
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

        if len(list_of_ids) > 0:
            face_recognition.encode_faces(user=user, face_name=face_name, pool_mode=True,
                                          pool_list=list_of_ids)
        else:
            face_recognition.encode_faces(user, face_name)

        result = face_recognition.recognize(image_content)
        status = result[0]['details']['name'] == face_name

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
