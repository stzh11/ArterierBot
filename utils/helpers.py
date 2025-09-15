import io
from aiogram import Bot
from settings import Settings
import logging
from utils.upload import upload_bytes_to_folder, ensure_folder_by_name
from aiogram.types import InputMediaPhoto

log = logging.getLogger(__name__)
def format_survey_for_sheets(data: dict) -> dict:
    mapping = {
        "q1_bought_art": Settings.q1_options,
        "q2_expertise": Settings.q2_options,
        "q3_difficulties": Settings.q3_options,
        "q4_what_to_search": Settings.q4_options,
        "q4_goal": Settings.q4_goal_options,
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
    bio = await bot.download_file(tg_file.file_path)  
    data = bio.getvalue()
    folder_son_id = await ensure_folder_by_name( folder_name=f"{file_name}_{user_id}", parent_id=folder_id)
    print("folder_son_id", folder_son_id)
    await upload_bytes_to_folder(filename=f"{file_name}_{file_id}", data = data, folder_id=folder_son_id)
    return f"https://drive.google.com/drive/folders/{folder_son_id}"

async def fetch_document_bytes_verbose(bot: Bot, file_id: str, name: str, mime: str):
    log.info("[TG] fetch document: file_id=%s name=%s mime=%s", file_id, name, mime)
    tg_file = await bot.get_file(file_id)
    log.info("[TG] doc path=%s file_id=%s", tg_file.file_path, tg_file.file_id)
    bio = await bot.download_file(tg_file.file_path)  # BytesIO
    data = bio.getvalue()
    log.info("[TG] doc bytes=%d", len(data))
    return {"name": name, "mime": mime or "application/octet-stream", "bytes": data}


def first_link(lst):
    for r in lst:
        if isinstance(r, str) and r:
            return r
    return ""

async def message_for_admin(data: dict, username: str, user__id: int) -> dict:
    coutry = data["q14_delivery_country"]
    what_to_search = data["q4_what_to_search"]
    colors = data["q5_colors"]
    mood = data["q8_mood"]
    artists = data["q6_favorite_authors"]
    wishes = data["q9_wishes"]
    budget = data["q13_budget"]
    size = data["q10_size"]
    message = f"Пользователь {user__id} с ником {username}\n\n" \
    f"Ты - опытный искусствовед и галерист. Надо найти в {coutry} {what_to_search} в тонах: {colors}, " \
    f"отражаюищих настроение {mood}. По стилю напоминает художников: {artists} Важно: {wishes}. Цена: {budget} Размеры: {size}"
    references_photos = []
    for photo in data["q7_references"]:
        references_photos.append(photo["file_id"])
    interior_photos = []
    for photo in data["q12_interior_photos"]:
        interior_photos.append(photo["file_id"])
    
    return {
        "message": message,
        "references_photos": references_photos,
        "interior_photos": interior_photos
    }

async def _send_album(bot: Bot, chat_id: int, file_ids: list[str], caption: str) -> None:
    if not file_ids:
        return
    if len(file_ids) == 1:
        await bot.send_photo(chat_id, file_ids[0], caption=caption)
        return
    for i in range(0, len(file_ids), 10):
        chunk = file_ids[i:i+10]
        media = [InputMediaPhoto(media=chunk[0], caption=caption)] + [
            InputMediaPhoto(media=fid) for fid in chunk[1:]
        ]
        await bot.send_media_group(chat_id, media)

async def notify_admins(bot: Bot, data: dict, username: str | None, user_id: int) -> None:
    pack = await message_for_admin(data, username, user_id)
    for admin_id in Settings.ADMIN_ACCOUNT_LIST:
        try:
            await bot.send_message(admin_id, "🆕 Новая анкета:")
            await bot.send_message(admin_id, pack["message"])

            await _send_album(bot, admin_id, pack["references_photos"], "Референсы")
            await _send_album(bot, admin_id, pack["interior_photos"], "Фото интерьера")
        except Exception as e:
            print(f"[notify_admins] failed for {admin_id}: {e}")