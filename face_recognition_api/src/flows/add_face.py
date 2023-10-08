import cv2
import os
import numpy as np
import time
from src.database.models.schema import User, Image
from src.cloud_bucket.bucket_actions import BucketActions


def add_face(path, image_bytes):
    try:
        encoded_image_bytes = write_image(path, image_bytes)
        BucketActions.upload_to_bucket(path, encoded_image_bytes)

    except Exception as e:
        print(e)


def write_image(path, image_bytes: bytes):
    image_data = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    _, encoded_image = cv2.imencode('.jpg', image)
    encoded_image_bytes = encoded_image.tobytes()
    return encoded_image_bytes
