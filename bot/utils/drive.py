# utils/drive.py
from __future__ import annotations

import io
import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

log = logging.getLogger(__name__)

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

def init_drive(creds_path: str):
    log.info("[DRIVE] init with creds: %s", creds_path)
    creds = Credentials.from_service_account_file(creds_path, scopes=DRIVE_SCOPES)
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    # Подскажи email сервис-аккаунта в лог:
    try:
        info = creds.service_account_email
        log.info("[DRIVE] service account: %s", info)
    except Exception:
        pass
    return service

def get_file_or_folder_meta(drive, file_id: str) -> dict:
    """Проверка доступности папки/файла."""
    meta = drive.files().get(fileId=file_id, fields="id,name,mimeType,owners,permissions").execute()
    return meta

async def upload_bytes_verbose(drive, *, name: str, mime: str, data: bytes, folder_id: str) -> dict:
    """
    Загружает файл. Возвращает {id, name, view}.
    """
    log.info("[DRIVE] uploading: name=%s mime=%s bytes=%d -> folder=%s", name, mime, len(data), folder_id)
    media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mime, resumable=False)
    body = {"name": name, "parents": [folder_id]}

    try:
        file = drive.files().create(
            body=body,
            media_body=media,
            fields="id,name,webViewLink"
        ).execute()
        log.info("[DRIVE] uploaded id=%s name=%s view=%s", file.get("id"), file.get("name"), file.get("webViewLink"))
        return {"id": file["id"], "name": file["name"], "view": file.get("webViewLink")}
    except HttpError as he:
        log.error("[DRIVE] HttpError on upload: %s", he, exc_info=True)
        raise
    except Exception as e:
        log.error("[DRIVE] Error on upload: %s", e, exc_info=True)
        raise

def ensure_view_permission(drive, file_id: str) -> Optional[str]:
    """
    Выставляет просмотр для всех (если политика проекта это допускает).
    Возвращает webViewLink.
    """
    try:
        drive.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
            fields="id"
        ).execute()
    except HttpError as he:
        # возможно уже есть права или запрещено политикой — не фатально
        log.warning("[DRIVE] set permission HttpError: %s", he)
    except Exception as e:
        log.warning("[DRIVE] set permission error: %s", e)

    try:
        meta = drive.files().get(fileId=file_id, fields="webViewLink").execute()
        return meta.get("webViewLink")
    except Exception:
        return None
