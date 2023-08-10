import cv2
import numpy as np
import time
from src.database.models.schema import User, Image



def add_face(path, image_bytes):
    try:
        write_image(path, image_bytes)

        return {"message": "success"}
    except Exception as e:
        print(e)
        return {"message": "failed"}


def write_image(path, image_bytes: bytes):
    image_data = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    cv2.imwrite(path, image)

