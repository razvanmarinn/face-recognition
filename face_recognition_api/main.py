from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.routers.face_recognition_router import recognition_router as face_recognition_router
from src.routers.face_emotion_router import face_emotion_router
from src.routers.share_pool import shared_image_pool_router
from src.database.models import models, schema
from src.database.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(face_recognition_router)
app.include_router(shared_image_pool_router)
app.include_router(face_emotion_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
