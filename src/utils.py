import google.auth
from google.auth import impersonated_credentials
import src.api_config as cfg


def auth_to_gcp():
    credentials, project_id = google.auth.default()
    target_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=cfg.service_account,
        target_scopes=target_scopes,
        lifetime=500)
    return project_id, target_credentials
