from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.connect_to_db import get_db
from src.jwt_handler import decode_jwt_token
from src.database.models.models import RecognitionHistory
from src.database.models.models import SharedImagePool

dashboard_router = APIRouter(prefix='/dashboards', tags=['dashboard'])


@dashboard_router.get("/get_succesful_recognitions")
async def get_succesful_recognitions(db: Session = Depends(get_db)):
    succesful_recognitions = db.query(RecognitionHistory).filter_by(success_status='t').count()
    failed_recognitions = db.query(RecognitionHistory).filter_by(success_status='f').count()
    return {"succesfull_recognitions": succesful_recognitions, "failed_recognitions": failed_recognitions}


@dashboard_router.get("/total_sips")
async def total_sips(db: Session = Depends(get_db)):
    total_sips = db.query(SharedImagePool).count()
    return {"total_sips": total_sips}
