from src.utils import auth_to_gcp
from google.cloud import storage
import src.api_config as cfg
import tempfile
import os
import cv2


class BucketActions:
    @staticmethod
    def get_images_from_folder(user_id: str, face_name: str):
        project_id, target_credentials = auth_to_gcp()
        client = storage.Client(credentials=target_credentials, project=project_id)
        bucket = client.get_bucket(cfg.BUCKET_NAME)

        prefix = f'faces/{user_id}/{face_name}/'

        blobs = bucket.list_blobs(prefix=prefix)
        temp_local_filenames = []

        temp_local_folder = tempfile.mkdtemp()

        for blob in blobs:
            image_filename = os.path.basename(blob.name)
            temp_local_filename = os.path.join(temp_local_folder, image_filename)
            blob.download_to_filename(temp_local_filename)
            temp_local_filenames.append(temp_local_filename)

        return temp_local_filenames, temp_local_folder

    @staticmethod
    def upload_to_bucket(path, image_bytes):
        project_id, target_credentials = auth_to_gcp()

        client = storage.Client(credentials=target_credentials, project=project_id)
        bucket = client.get_bucket(cfg.BUCKET_NAME)

        blob = bucket.blob(path)
        blob.upload_from_string(image_bytes)

        print(f"Uploaded {path} to the bucket")
