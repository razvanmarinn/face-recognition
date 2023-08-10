from src.face_recognition import FaceRecognition
from src.flows.add_face import add_face
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.upload_to_db import create_user_item
from src.database.models import models, schema
from src.database.database import SessionLocal, engine
from src.database.models.schema import Image, ImageCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/face_recognition/add_face")
async def face_recognition_add_face(name: str = Form(...), image: UploadFile = File(...),
                                    db: Session = Depends(get_db)):
    image_content = await image.read()
    file_size = len(image_content)
    image = Image(name=name, size=file_size, user_id=10)
    add_face(image.path, image_content)
    create_user_item(db=db, item=image)
    return {"message": "success"}
