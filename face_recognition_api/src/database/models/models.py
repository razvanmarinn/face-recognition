from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from src.database.database import Base


class Image(Base):
    __tablename__ = "image_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, index=True)
    size = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))


class RecognitionHistory(Base):
    __tablename__ = "recognize_runs_hist"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    face_name = Column(String, index=True)
    timestamp = Column(Float, index=True)
    success_status = Column(Boolean, index=True)
