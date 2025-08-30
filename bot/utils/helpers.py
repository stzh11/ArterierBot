import io
from aiogram import Bot
from settings import Settings


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


async def fetch_photo_bytes(bot: Bot, photo, *, fallback_name: str = "photo.jpg"):
    # PhotoSize не содержит имени файла → дадим своё
    name = fallback_name
    mime = "image/jpeg"
    file = await bot.get_file(photo.file_id)
    buf = io.BytesIO()
    await bot.download(file, destination=buf)
    return {"name": name, "mime": mime, "bytes": buf.getvalue()}

async def fetch_document_bytes(bot: Bot, doc):
    name = doc.file_name or "document"
    mime = doc.mime_type or "application/octet-stream"
    file = await bot.get_file(doc.file_id)
    buf = io.BytesIO()
    await bot.download(file, destination=buf)
    return {"name": name, "mime": mime, "bytes": buf.getvalue()}