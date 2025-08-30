# services/uploader.py
from __future__ import annotations
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from settings import Settings
from utils.drive import init_drive, upload_bytes
from utils.helpers import fetch_photo_bytes, fetch_document_bytes

_drive = None
def get_drive():
    global _drive
    if _drive is None:
        _drive = init_drive(Settings.GOOGLE_CREDS)
    return _drive

async def upload_state_files_to_drive(bot: Bot, state: FSMContext, key: str, *, folder_id: str) -> list[dict]:
    """
    key: 'q7_files' или 'q12_files'
    Возвращает список словарей {'name','link','id'}
    """
    data = await state.get_data()
    files = data.get(key, [])
    if not files:
        return []

    drive = get_drive()
    uploaded = []

    for f in files:
        kind = f.get("kind")
        if kind == "photo":
            payload = await fetch_photo_bytes(bot, type("P", (), {"file_id": f["file_id"]})(), fallback_name=f"photo_{['file_id'][-8:]}.jpg")
        elif kind == "document":
            # тут лучше сохранять в state name/mime при приёме
            doc_stub = type("D", (), {
                "file_id": f["file_id"],
                "file_name": f.get("name") or f"file_{['file_id'][-8:]}",
                "mime_type": f.get("mime") or "application/octet-stream"
            })()
            payload = await fetch_document_bytes(bot, doc_stub)
        else:
            continue

        r = await upload_bytes(drive, name=payload["name"], mime=payload["mime"], data=payload["bytes"], folder_id=folder_id)
        uploaded.append({"name": payload["name"], "id": r["id"], "link": r["view"]})

    # сохраним обратно (например, как '<key>_links')
    data[f"{key}_links"] = uploaded
    await state.set_data(data)
    return uploaded
