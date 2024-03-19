from fastapi import FastAPI
from src.db.models import models
from src.db.login_database import engine
from src.routers.login_router import login_router
from src.routers.user_details_router import user_details_routers
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(login_router)
app.include_router(user_details_routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)
