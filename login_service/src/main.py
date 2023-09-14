from fastapi import FastAPI
from src.db.models import models
from src.db.login_database import engine
from src.routers.login_router import login_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(login_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)
