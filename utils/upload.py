# utils/upload.py
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import asyncio
from googleapiclient.http import MediaIoBaseUpload
from utils.drive import service as default_service  # твой построенный Drive service

# Один общий поток для всех запросов к Google API
_GOOGLE_EXECUTOR = ThreadPoolExecutor(max_workers=1)

# ========= СИНХРОННЫЕ ФУНКЦИИ =========

def ensure_folder_by_name_sync(service, folder_name: str, parent_id: str | None = None) -> str:
    FOLDER_MIME = "application/vnd.google-apps.folder"

    def _escape(s: str) -> str:
        return s.replace("'", "\\'")

    def _get_or_create_arterier_root() -> str:
        q = (
            f"mimeType = '{FOLDER_MIME}' and "
            "name = 'Arterier' and trashed = false and 'root' in parents"
        )
        resp = service.files().list(q=q, fields="files(id)", pageSize=1).execute()
        files = resp.get("files", [])
        if files:
            return files[0]["id"]
        body = {"name": "Arterier", "mimeType": FOLDER_MIME, "parents": ["root"]}
        created = service.files().create(body=body, fields="id").execute()
        return created["id"]

    def _is_descendant_of(node_id: str, ancestor_id: str) -> bool:
        cur = node_id
        seen = set()
        while cur and cur not in seen:
            seen.add(cur)
            info = service.files().get(fileId=cur, fields="id, parents").execute()
            parents = info.get("parents", [])
            if ancestor_id in parents:
                return True
            cur = parents[0] if parents else None
        return False

    arterier_id = _get_or_create_arterier_root()
    actual_parent_id = parent_id if (parent_id and _is_descendant_of(parent_id, arterier_id)) else arterier_id

    q = (
        f"mimeType = '{FOLDER_MIME}' and "
        f"name = '{_escape(folder_name)}' and trashed = false and "
        f"'{actual_parent_id}' in parents"
    )
    resp = service.files().list(q=q, fields="files(id)", pageSize=1).execute()
    files = resp.get("files", [])
    if files:
        return files[0]["id"]

    metadata = {"name": folder_name, "mimeType": FOLDER_MIME, "parents": [actual_parent_id]}
    created = service.files().create(body=metadata, fields="id").execute()
    return created["id"]


def upload_bytes_to_folder_sync(
    service,
    data: bytes,
    filename: str,
    folder_id: str,
    mime_type: str = "application/octet-stream",
):
    file_obj = BytesIO(data)
    media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)
    metadata = {"name": filename, "parents": [folder_id]}
    created = service.files().create(
        body=metadata,
        media_body=media,
        fields="id, name, webViewLink",
    ).execute()
    return created


# ========= БЕЗОПАСНЫЕ ASYNC-ОБЁРТКИ (1 поток) =========

async def ensure_folder_by_name(
    folder_name: str,
    parent_id: str | None = None,
    service=default_service,
) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _GOOGLE_EXECUTOR, ensure_folder_by_name_sync, service, folder_name, parent_id
    )


async def upload_bytes_to_folder(
    data: bytes,
    filename: str,
    folder_id: str,
    mime_type: str = "application/octet-stream",
    service=default_service,
):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _GOOGLE_EXECUTOR, upload_bytes_to_folder_sync, service, data, filename, folder_id, mime_type
    )
