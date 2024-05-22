from src.utils import auth_to_gcp
from google.cloud import storage
import src.api_config as cfg
import tempfile
import os
import cv2
import datetime


class BucketActions:
    @staticmethod
    def get_images_from_folder(user_id: str = None, pool_id: int = None, face_name: str = None, pool_mode: bool = False,
                               path: str = None, face_auth: bool = False):
        try:
            project_id, target_credentials = auth_to_gcp()
            client = storage.Client(credentials=target_credentials, project=project_id)
            bucket = client.get_bucket(cfg.BUCKET_NAME)
            prefix = (
                f'faces/{user_id}/{face_name}/' if (not pool_mode and not face_auth) else
                (f'shared_pool_images/{pool_id}/{face_name}/' if pool_mode else
                 f'faces/{user_id}/face_auth')  # to be looked at, it is bugged
            )

            blobs = bucket.list_blobs(prefix=prefix)

            temp_local_filenames = []

            if path is None:
                temp_local_folder = tempfile.mkdtemp()
            else:
                temp_local_folder = path

            for blob in blobs:
                image_filename = os.path.basename(blob.name)
                temp_local_filename = os.path.join(temp_local_folder, image_filename)
                blob.download_to_filename(temp_local_filename)
                temp_local_filenames.append(temp_local_filename)

            return temp_local_filenames, temp_local_folder

        except Exception as e:
            print(f"Error in get_images_from_folder: {str(e)}")
            return [], None

    @staticmethod
    def get_images_for_identification(user_id: int):
        try:
            project_id, target_credentials = auth_to_gcp()
            client = storage.Client(credentials=target_credentials, project=project_id)
            bucket = client.get_bucket(cfg.BUCKET_NAME)
            prefix = f'faces/{user_id}/'

            blobs = bucket.list_blobs(prefix=prefix)

            temp_local_filenames = []
            temp_local_folder = tempfile.mkdtemp()

            for blob in blobs:
                if not blob.name.startswith(f'faces/{user_id}/face_auth/'):
                    path_parts = os.path.split(blob.name)
                    directory_before = os.path.basename(os.path.dirname(blob.name))
                    image_filename = path_parts[1]
                    actual_path = os.path.join(directory_before, image_filename)

                    # Create the directory if it does not exist
                    full_local_path = os.path.join(temp_local_folder, directory_before)
                    os.makedirs(full_local_path, exist_ok=True)

                    temp_local_filename = os.path.join(full_local_path, image_filename)
                    blob.download_to_filename(temp_local_filename)
                    temp_local_filenames.append(temp_local_filename)

            return temp_local_filenames, temp_local_folder

        except Exception as e:
            print(f"Error in get_images_for_identification: {str(e)}")
            return [], None

    @staticmethod
    def upload_to_bucket(path, image_bytes):
        project_id, target_credentials = auth_to_gcp()

        client = storage.Client(credentials=target_credentials, project=project_id)
        bucket = client.get_bucket(cfg.BUCKET_NAME)

        blob = bucket.blob(path)
        blob.upload_from_string(image_bytes)

        print(f"Uploaded {path} to the bucket")

    @staticmethod
    def copy_within_bucket(source_folder, destination_folder):
        project_id, target_credentials = auth_to_gcp()
        client = storage.Client(credentials=target_credentials, project=project_id)
        bucket = client.get_bucket(cfg.BUCKET_NAME)

        source_blobs = bucket.list_blobs(prefix=source_folder)

        for source_blob in source_blobs:
            destination_blob = bucket.blob(destination_folder + '/' + source_blob.name[len(source_folder):])

            temp_filename = os.path.join(tempfile.gettempdir(), 'temporary_file')

            source_blob.download_to_filename(temp_filename)

            destination_blob.upload_from_filename(temp_filename)

            os.remove(temp_filename)

    @staticmethod
    def retrieve_all_image_urls(face_name: str, user_id: str):
        project_id, target_credentials = auth_to_gcp()
        client = storage.Client(credentials=target_credentials, project=project_id)
        bucket = client.get_bucket(cfg.BUCKET_NAME)

        prefix = f'faces/{face_name}/{user_id}/'

        blobs = bucket.list_blobs(prefix=prefix)

        image_urls = []
        for blob in blobs:
            signed_url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=60))
            image_urls.append(signed_url)

        return image_urls
