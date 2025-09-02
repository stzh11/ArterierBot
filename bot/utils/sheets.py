
import asyncio
import gspread
from datetime import datetime
import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest
import os
from pathlib import Path
from gspread.exceptions import APIError
import gspread
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    ]

def init_sheets(spreadsheet_name: str):
    token_path = Path("/Users/stepanzukov/Desktop/Projects/Arterier/bot/token.json")
    secret_path = Path("/Users/stepanzukov/Desktop/Projects/Arterier/client_secret.json")

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    def _run_oauth_flow():
        flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
        # офлайн-рефреш и форс-консент, чтобы точно выдать новые скоупы
        return flow.run_local_server(port=0, access_type="offline", prompt="consent")

    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(GoogleRequest())
            else:
                creds = _run_oauth_flow()
        except RefreshError:
            # чаще всего именно тут и случается invalid_scope
            if token_path.exists():
                token_path.unlink(missing_ok=True)
            creds = _run_oauth_flow()

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
    print("TOKEN FILE:", token_path, "exists:", os.path.exists(token_path))
    print("GRANTED SCOPES:", getattr(creds, "scopes", None))
    print("VALID:", creds.valid, "EXPIRED:", creds.expired, "REFRESH_TOKEN:", bool(getattr(creds, "refresh_token", None)))
    client = gspread.authorize(creds)
    sh = client.open(spreadsheet_name)
    return sh.sheet1


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

async def ensure_header_async(ws) -> None:
    values = await asyncio.to_thread(ws.get_all_values)
    if not values:
        try:
            await asyncio.to_thread(ws.append_row, HEADERS, value_input_option="USER_ENTERED")
        except APIError as e:
            # Если параллельно уже кто-то успел написать хедер — просто игнорируем конфликт
            if "Already exists" in str(e) or "invalid" in str(e):
                return
            raise

async def save_survey(ws, data: dict, user_id: int, username: str | None) -> None:
    await ensure_header_async(ws)

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
        data.get("q7_folder_link", ""),
        data.get("q8_mood", ""),
        data.get("q9_wishes", ""),
        _join(data.get("q10_size")),
        _join(data.get("q11_format")),
        data.get("q12_folder_link", ""),
        data.get("q13_budget", ""),
        data.get("q14_delivery_country", ""),
        _join(data.get("q15_hobbies")),
        data.get("q16_contact_method", ""),
        data.get("q17_contact_details", ""),
    ]

    # Небольшой ретрай на случай 429/500/503 от API
    backoff = 0.5
    for attempt in range(4):
        try:
            await asyncio.to_thread(ws.append_row, row, value_input_option="USER_ENTERED")
            return
        except APIError as e:
            s = str(e)
            transient = any(x in s for x in ("rateLimitExceeded", "internalError", "backendError", "quotaExceeded", "503", "500"))
            if attempt < 3 and transient:
                await asyncio.sleep(backoff)
                backoff *= 2
                continue
            raise