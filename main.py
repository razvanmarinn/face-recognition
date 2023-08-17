from src.flows.recognize import FaceRecognition
from src.flows.add_face import add_face
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.upload_to_db import upload_path_to_db
from src.database.models import models, schema
from src.database.database import SessionLocal, engine
from src.database.models.schema import Image, ImageCreate, User
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
face_recognition = FaceRecognition()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/face_recognition/add_face")
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


@app.post("/face_recognition/recognize")
async def recognize(face_name: str = Form(...), image: UploadFile = File(...)):
    image_content = await image.read()
    file_size = len(image_content)
    user = User(id=10, email="test", password="test", username="test")
    image = Image(name="temp", size=file_size, user_id=user.id)
    face_recognition.encode_faces(user, face_name)
    return face_recognition.run_recognition(image_content)
