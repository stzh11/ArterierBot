import argparse
from io import BytesIO
import mimetypes
import os
import sys
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# Полный доступ для простоты интеграции (поиск папок, загрузка файлов и т.д.)
SCOPES = ["https://www.googleapis.com/auth/drive"]

TOKEN_PATH = "token.json"
CLIENT_SECRET_PATH = "/Users/stepanzukov/Desktop/Projects/Arterier/client_secret.json"


def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def ensure_folder_by_name(service, folder_name, parent_id=None):
    q_parts = [
        "mimeType = 'application/vnd.google-apps.folder'",
        f"name = '{folder_name}'",
        "trashed = false",
    ]
    if parent_id:
        q_parts.append(f"'{parent_id}' in parents")
    q = " and ".join(q_parts)

    resp = service.files().list(q=q, fields="files(id, name)", pageSize=10).execute()
    files = resp.get("files", [])
    if files:
        return files[0]["id"]

    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    created = service.files().create(body=metadata, fields="id").execute()
    return created["id"]



def upload_bytes_to_folder(service, data: bytes, filename: str, folder_id: str, mime_type="application/octet-stream"):
    file_obj = BytesIO(data)
    media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)

    metadata = {
        "name": filename,
        "parents": [folder_id],
    }

    created = service.files().create(body=metadata, media_body=media, fields="id, name, webViewLink").execute()
    return created

service = get_drive_service()