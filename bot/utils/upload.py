# services/uploader.py
from __future__ import annotations

import logging
import re
import time
from typing import Any, Dict, List, Tuple

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from googleapiclient.errors import HttpError

from settings import Settings
from utils.drive import init_drive, ensure_view_permission, upload_bytes_verbose, get_file_or_folder_meta
from utils.helpers import fetch_photo_bytes_verbose, fetch_document_bytes_verbose

log = logging.getLogger(__name__)

# --- Lazy singleton для Google Drive ---
_drive = None

def get_drive():
    """Инициализация клиента Drive один раз за процесс."""
    global _drive
    if _drive is None:
        log.info("[DRIVE] init_drive(%s)", Settings.GOOGLE_CREDS)
        _drive = init_drive(Settings.GOOGLE_CREDS)
        log.info("[DRIVE] client ready")
    return _drive


_FOLDER_ID_RE = re.compile(r"/folders/([a-zA-Z0-9_\-]+)")

def normalize_folder_id(folder_id_or_url: str) -> str:
    """
    Принимает либо чистый ID, либо URL папки в Drive.
    Возвращает ID папки.
    """
    if not folder_id_or_url:
        return ""
    m = _FOLDER_ID_RE.search(folder_id_or_url)
    if m:
        return m.group(1)
    return folder_id_or_url.strip()


async def upload_state_files_to_drive(
    bot: Bot,
    state: FSMContext,
    key: str,                 # 'q7_files' или 'q12_files'
    *,
    folder_id: str,           # может прийти URL — нормализуем
    preflight: bool = True,   # проверить доступ к папке перед загрузкой
) -> List[Dict[str, Any]]:
    """
    Берёт из FSM state список файлов под ключом `key`,
    скачивает их из Telegram и загружает в указанную папку Google Drive.

    В state[key] ожидаются элементы:
      {"kind": "photo", "file_id": "...", "size": int?}
      {"kind": "document", "file_id": "...", "name": "...", "mime": "...", "size": int?}

    Возвращает список [{'name','id','link'}] и сохраняет его в state как f"{key}_links".
    """

    t0 = time.perf_counter()
    raw_folder = folder_id
    folder_id = normalize_folder_id(folder_id)
    log.info("[UPLOADER] start key=%s, raw_folder=%s -> folder_id=%s", key, raw_folder, folder_id)

    if not folder_id:
        log.error("[UPLOADER] Empty folder_id for key=%s. STOP.", key)
        return []

    drive = get_drive()

    # --- Preflight: есть ли доступ к папке? ---
    if preflight:
        try:
            meta = get_file_or_folder_meta(drive, folder_id)
            log.info("[UPLOADER] preflight ok: folder id=%s, name=%s, mime=%s", meta.get("id"), meta.get("name"), meta.get("mimeType"))
        except HttpError as he:
            log.error("[UPLOADER] preflight HttpError: %s", he, exc_info=True)
            return []
        except Exception as e:
            log.error("[UPLOADER] preflight error: %s", e, exc_info=True)
            return []

    data = await state.get_data()
    files = data.get(key, [])
    log.info("[UPLOADER] files count in state[%s]: %s", key, len(files))

    if not files:
        return []

    uploaded: List[Dict[str, Any]] = []

    for idx, f in enumerate(files, start=1):
        t_file = time.perf_counter()
        try:
            kind = f.get("kind")
            file_id = f.get("file_id")
            size = f.get("size")

            log.info("[UPLOADER] #%d kind=%s file_id=%s size=%s", idx, kind, file_id, size)

            if not file_id:
                log.warning("[UPLOADER] #%d skip: no file_id", idx)
                continue

            # 1) Скачиваем байты из TG
            if kind == "photo":
                payload = await fetch_photo_bytes_verbose(
                    bot=bot,
                    file_id=file_id,
                    fallback_name=f"photo_{file_id[-8:]}.jpg",
                )
            elif kind == "document":
                name = f.get("name") or f"file_{file_id[-8:]}"
                mime = f.get("mime") or "application/octet-stream"
                payload = await fetch_document_bytes_verbose(
                    bot=bot,
                    file_id=file_id,
                    name=name,
                    mime=mime,
                )
            else:
                log.warning("[UPLOADER] #%d skip: unknown kind '%s'", idx, kind)
                continue

            log.info("[UPLOADER] #%d TG bytes ready: name=%s, mime=%s, bytes=%d",
                     idx, payload["name"], payload["mime"], len(payload["bytes"]))

            # 2) Грузим в Drive
            res = await upload_bytes_verbose(
                drive=drive,
                name=payload["name"],
                mime=payload["mime"],
                data=payload["bytes"],
                folder_id=folder_id,
            )

            log.info("[UPLOADER] #%d Drive uploaded: id=%s name=%s view=%s",
                     idx, res.get("id"), res.get("name"), res.get("view"))

            # 3) Делаем публичный просмотр (если включено)
            try:
                link = ensure_view_permission(drive, res["id"]) or res.get("view")
            except HttpError as he:
                log.error("[UPLOADER] #%d set permission HttpError: %s", idx, he, exc_info=True)
                link = res.get("view")
            except Exception as e:
                log.error("[UPLOADER] #%d set permission error: %s", idx, e, exc_info=True)
                link = res.get("view")

            uploaded.append({"name": res.get("name"), "id": res.get("id"), "link": link})

            dt = (time.perf_counter() - t_file) * 1000
            log.info("[UPLOADER] #%d done in %.1f ms", idx, dt)

        except HttpError as he:
            log.error("[UPLOADER] #%d HttpError: %s", idx, he, exc_info=True)
        except Exception as e:
            log.error("[UPLOADER] #%d error: %s", idx, e, exc_info=True)

    # 4) сохраним ссылки в state
    data[f"{key}_links"] = uploaded
    await state.set_data(data)
    total_ms = (time.perf_counter() - t0) * 1000
    log.info("[UPLOADER] finished key=%s: uploaded=%d in %.1f ms", key, len(uploaded), total_ms)

    return uploaded
