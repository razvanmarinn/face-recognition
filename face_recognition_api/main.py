from fastapi import FastAPI, Depends
from src.routers.face_recognition_router import recognition_router as face_recognition_router
from src.routers.share_pool import shared_image_pool_router
from src.database.models import models, schema
from src.database.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(face_recognition_router)
app.include_router(shared_image_pool_router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
