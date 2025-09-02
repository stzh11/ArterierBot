import io
from aiogram import Bot
from settings import Settings
import logging
from utils.upload import upload_bytes_to_folder, ensure_folder_by_name, service
log = logging.getLogger(__name__)
def format_survey_for_sheets(data: dict) -> dict:
    mapping = {
        "q1_bought_art": Settings.q1_options,
        "q2_expertise": Settings.q2_options,
        "q3_difficulties": Settings.q3_options,
        "q4_what_to_search": Settings.q4_options,
        "q5_colors": Settings.q5_options,
        "q10_size": Settings.q10_options,
        "q11_format": Settings.q11_options,
        "q13_budget": Settings.q13_options,
        "q15_hobbies": Settings.q15_options,
    }

    result = {}

    for key, value in data.items():
        if key in mapping:
            options = dict(mapping[key]) 
            if isinstance(value, list):
                result[key] = ", ".join([options.get(v, v) for v in value])
            else:
                result[key] = options.get(value, value)

        elif key in ["q6_favorite_authors", "q8_mood", "q9_wishes", "q14_delivery_country", "q17_contact_details"]:
            result[key] = value

        elif key in ["q7_files", "q12_files"]:
            result[key] = ", ".join([f["file_id"] for f in value])

        else:
            result[key] = value

    return result


async def fetch_photo_bytes_verbose(bot: Bot, file_id: str, user_id:str = "", folder_id:str = "", file_name: str = ""):
    log.info("[TG] fetch photo: file_id=%s", file_id)
    tg_file = await bot.get_file(file_id)
    log.info("[TG] photo path=%s file_id=%s", tg_file.file_path, tg_file.file_id)
    bio = await bot.download_file(tg_file.file_path)  # BytesIO
    data = bio.getvalue()
    folder_son_id = ensure_folder_by_name(service=service, folder_name=f"{file_name}_{user_id}", parent_id=folder_id)
    upload_bytes_to_folder(filename=f"{file_name}_{user_id}", data = data, folder_id=folder_son_id, service=service)["webViewLink"]
    return f"https://drive.google.com/drive/folders/{folder_son_id}"

async def fetch_document_bytes_verbose(bot: Bot, file_id: str, name: str, mime: str):
    log.info("[TG] fetch document: file_id=%s name=%s mime=%s", file_id, name, mime)
    tg_file = await bot.get_file(file_id)
    log.info("[TG] doc path=%s file_id=%s", tg_file.file_path, tg_file.file_id)
    bio = await bot.download_file(tg_file.file_path)  # BytesIO
    data = bio.getvalue()
    log.info("[TG] doc bytes=%d", len(data))
    return {"name": name, "mime": mime or "application/octet-stream", "bytes": data}