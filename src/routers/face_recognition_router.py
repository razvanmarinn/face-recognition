from fastapi import APIRouter, UploadFile, File, Form, Depends
from src.database.connect_to_db import get_db
from sqlalchemy.orm import Session
from src.flows.recognize import FaceRecognition
from src.flows.add_face import add_face
from src.database.upload_to_db import upload_path_to_db
from src.database.models.schema import Image, ImageCreate, User

recognition_router = APIRouter(prefix='/face_recognition', tags=['face_recognition'] )

face_recognition = FaceRecognition()


@recognition_router.post("/add_face")
async def face_recognition_add_face(name: str = Form(...), image: UploadFile = File(...),
                                    db: Session = Depends(get_db)):
    try:
        image_content = await image.read()
        file_size = len(image_content)
        image = Image(name=name, size=file_size, user_id=11)
        add_face(image.path, image_content)
        upload_path_to_db(db=db, item=image)
        return {"message": "success"}
    except Exception as e:
        return {"message": e}


@recognition_router.post("/recognize")
async def recognize(face_name: str = Form(...), image: UploadFile = File(...)):
    image_content = await image.read()
    file_size = len(image_content)
    user = User(id=11, email="test", password="test", username="test")
    image = Image(name="temp", size=file_size, user_id=user.id)
    face_recognition.encode_faces(user, face_name)
    return face_recognition.recognize(image_content)
