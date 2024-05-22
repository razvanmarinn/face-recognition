import google.auth
from google.auth import impersonated_credentials
import src.api_config as cfg
import os
import bcrypt


def auth_to_gcp():
    credentials, project_id = google.auth.default()
    target_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=cfg.SERVICE_ACCOUNT_GCS,
        target_scopes=target_scopes,
        lifetime=500)
    return project_id, target_credentials


# def delete_temp_files(temp_local_folder):
#     for file in os.listdir(temp_local_folder):
#         file_path = os.path.join(temp_local_folder, file)
#         try:
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#         except Exception as e:
#             print(e)
#     os.rmdir(temp_local_folder)
#     print("Deleted temp files")


def delete_temp_files(folder_path: str):
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(folder_path)
    except Exception as e:
        print(f"Error deleting temp files: {str(e)}")