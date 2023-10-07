from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from src.database.database import Base


class Image(Base):
    __tablename__ = "image_locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    path = Column(String, index=True)
    size = Column(Float)
    user_id = Column(Integer)


class RecognitionHistory(Base):
    __tablename__ = "recognize_runs_hist"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    user_id = Column(Integer)
    face_name = Column(String, index=True)
    timestamp = Column(Float, index=True)
    success_status = Column(Boolean, index=True)

class SharedImagePool(Base):
    __tablename__ = "shared_image_pool"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer)
    image_pool_name = Column(String, index=True)


class SharedImagePoolFaces(Base):
    __tablename__ = "shared_image_pool_faces"

    id = Column(Integer, primary_key=True, index=True)
    image_pool_id = Column(Integer)
    user_id = Column(Integer)
    face_name = Column(String, index=True)

class SharedImagePoolMembers(Base):
    __tablename__ = "shared_image_pool_members"

    id = Column(Integer, primary_key=True, index=True)
    image_pool_id = Column(Integer)
    user_id = Column(Integer)

class SharedImagePoolPermissions(Base):
    __tablename__ = "shared_image_pool_permissions"

    id = Column(Integer, primary_key=True, index=True)
    image_pool_id = Column(Integer)
    user_id = Column(Integer)
    read = Column(Boolean)
    write = Column(Boolean)
    delete = Column(Boolean)