
from __future__ import annotations
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials
import io
import asyncio

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

def init_drive(creds_path: str):
    creds = Credentials.from_service_account_file(creds_path, scopes=DRIVE_SCOPES)
    return build("drive", "v3", credentials=creds)

def _upload_bytes_sync(drive, *, name: str, mime: str, data: bytes, folder_id: str):
    media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mime, resumable=False)
    meta = {"name": name, "parents": [folder_id]}
    file = drive.files().create(body=meta, media_body=media, fields="id, webViewLink, webContentLink").execute()
    # сделать доступ по ссылке (просмотр)
    drive.permissions().create(fileId=file["id"], body={"type": "anyone", "role": "reader"}).execute()
    return {"id": file["id"], "view": file["webViewLink"], "download": file.get("webContentLink")}

async def upload_bytes(drive, *, name: str, mime: str, data: bytes, folder_id: str):
    return await asyncio.to_thread(_upload_bytes_sync, drive, name=name, mime=mime, data=data, folder_id=folder_id)
