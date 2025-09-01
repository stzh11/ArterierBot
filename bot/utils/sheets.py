import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def init_sheets(spreadsheet_name: str):
    creds = None
    token_path = "/Users/stepanzukov/Desktop/Projects/Arterier/bot/token.json"
    secret_path = "/Users/stepanzukov/Desktop/Projects/Arterier/client_secret.json"

    # 1. Пробуем загрузить готовый токен
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # 2. Если нет токена или он недействителен → обновляем / создаём заново
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())   # тут важно скобки
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    # 3. Авторизация через gspread
    client = gspread.authorize(creds)
    sh = client.open(spreadsheet_name)
    ws = sh.sheet1  # или sh.worksheet("Лист1")
    return ws

HEADERS = [
    "timestamp",
    "user_id",
    "username",
    "q1_bought_art",
    "q2_expertise",
    "q3_difficulties",
    "q4_goal",
    "q4_what_to_search",
    "q5_colors",
    "q6_favorite_authors",
    "q7_references",       
    "q8_mood",
    "q9_wishes",
    "q10_size",
    "q11_format",
    "q12_interior_photos",    
    "q13_budget",
    "q14_delivery_country",
    "q15_hobbies",
    "q16_contact_method",
    "q17_contact_details",
]

def _join(value):
    if value is None:
        return ""
    if isinstance(value, (list, set, tuple)):
        return ", ".join(map(str, value))
    return str(value)

def _files_to_str(files):
    if not files:
        return ""
    return ", ".join(f.get("file_id", "") for f in files if isinstance(f, dict))

def ensure_header(ws):
    values = ws.get_all_values()
    if not values:
        ws.append_row(HEADERS, value_input_option="USER_ENTERED")

def _drive_links_to_str(objs):
    if not objs:
        return ""
    # красиво: =HYPERLINK("url","name")
    return ", ".join([f'=HYPERLINK("{o["link"]}","{o["name"]}")' for o in objs if "link" in o])


def save_survey(ws, data: dict, user_id: int, username: str | None):
    ensure_header(ws)
    row = [
        datetime.now().isoformat(timespec="seconds"),
        str(user_id),
        username or "",
        data.get("q1_bought_art", ""),
        data.get("q2_expertise", ""),
        _join(data.get("q3_difficulties")),
        _join(data.get("q4_goal")),
        _join(data.get("q4_what_to_search")),
        _join(data.get("q5_colors")),
        data.get("q6_favorite_authors", ""),
        _drive_links_to_str(data.get("q7_files_links")) or _files_to_str(data.get("q7_files")),
        data.get("q8_mood", ""),
        data.get("q9_wishes", ""),
        _join(data.get("q10_size")),
        _join(data.get("q11_format")),
        _drive_links_to_str(data.get("q12_files_links")) or _files_to_str(data.get("q12_files")),
        data.get("q13_budget", ""),
        data.get("q14_delivery_country", ""),
        _join(data.get("q15_hobbies")),
        data.get("q16_contact_method", ""),
        data.get("q17_contact_details", ""),
    ]
    ws.append_row(row, value_input_option="USER_ENTERED")