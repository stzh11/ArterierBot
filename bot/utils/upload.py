
from io import BytesIO
import os
import asyncio
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest



SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    ]

TOKEN_PATH = "/Users/stepanzukov/Desktop/Projects/Arterier/bot/token.json"
CLIENT_SECRET_PATH = "/Users/stepanzukov/Desktop/Projects/Arterier/client_secret.json"


def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)



async def ensure_folder_by_name(service, folder_name: str, parent_id: str | None = None) -> str:
    def _sync():
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

    return await asyncio.to_thread(_sync)


async def upload_bytes_to_folder(
    service,
    data: bytes,
    filename: str,
    folder_id: str,
    mime_type: str = "application/octet-stream",
):
    def _sync():
        file_obj = BytesIO(data)
        media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)
        metadata = {"name": filename, "parents": [folder_id]}
        created = service.files().create(
            body=metadata,
            media_body=media,
            fields="id, name, webViewLink",
        ).execute()
        return created

    return await asyncio.to_thread(_sync)

service = get_drive_service()