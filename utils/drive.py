
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest
from settings import Settings
from pathlib import Path

def get_drive_service(token_path: Path, scopes: list[str], client_secret_path: Path):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)

service = get_drive_service(token_path=Settings.GOOGLE_AUTH_TOKEN_PATH, client_secret_path=Settings.GOOGLE_CLIENT_SECRET_PATH, scopes=Settings.SCOPES)