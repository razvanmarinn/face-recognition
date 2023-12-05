from fastapi import FastAPI
from src.db.models import models
from src.db.login_database import engine
from src.routers.login_router import login_router
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(login_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can specify specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)
