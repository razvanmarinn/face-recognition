from google.cloud import storage
from src.utils import auth_to_gcp
import os
import tempfile


def upload_to_bucket(path, image_bytes):
    project_id, target_credentials = auth_to_gcp()

    client = storage.Client(credentials=target_credentials, project=project_id)
    bucket = client.get_bucket('face-recognition-bucket-proj')

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(image_bytes)
        temp_path = temp_file.name

    try:
        blob = bucket.blob(path)
        blob.upload_from_filename(temp_path)
        print(f"Uploaded {path} to the bucket")
    finally:
        os.remove(temp_path)
