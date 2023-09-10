from fastapi import FastAPI, Depends
from src.database.models import models, schema
from src.database.database import engine
from src.routers.login_router import login_router
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(login_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)
