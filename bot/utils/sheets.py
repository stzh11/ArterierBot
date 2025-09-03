import asyncio
from pathlib import Path
from datetime import datetime
import gspread
from gspread.exceptions import APIError, WorksheetNotFound
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest
from google.auth.exceptions import RefreshError

HEADERS = [
    "timestamp","user_id","username","q1_bought_art","q2_expertise","q3_difficulties",
    "q4_goal","q4_what_to_search","q5_colors","q6_favorite_authors","q7_references",
    "q8_mood","q9_wishes","q10_size","q11_format","q12_interior_photos",
    "q13_budget","q14_delivery_country","q15_hobbies","q16_contact_method","q17_contact_details",
]

def _join(v):
    if v is None: return ""
    if isinstance(v, (list, tuple, set)): return ", ".join(map(str, v))
    return str(v)

def init_sheets(*, spreadsheet_id: str, worksheet_title: str | None = None,
                worksheet_gid: int | None = None, scopes: list[str],
                token_path: str, secret_path: str):
    token_path = Path(token_path)
    secret_path = Path(secret_path)

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    def _flow():
        flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), scopes)
        return flow.run_local_server(port=0, access_type="offline", prompt="consent")

    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(GoogleRequest())
            else:
                creds = _flow()
        except RefreshError:
            token_path.unlink(missing_ok=True)
            creds = _flow()

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    client = gspread.authorize(creds)
    sh = client.open_by_key(spreadsheet_id)
    print(f"[Sheets] Using spreadsheet: {sh.title}  {sh.url}")

    ws = None
    if worksheet_gid is not None:
        ws = sh.get_worksheet_by_id(worksheet_gid)
    elif worksheet_title:
        try:
            ws = sh.worksheet(worksheet_title)
        except WorksheetNotFound:
            ws = sh.add_worksheet(title=worksheet_title, rows=1000, cols=26)
    else:
        ws = sh.sheet1

    print(f"[Sheets] Using worksheet: {ws.title} (gid={ws.id})")
    return ws

from settings import Settings

SHEET = init_sheets(
    spreadsheet_id="12Ca1baxvzfOQMOHX_YGhO-u0EfnowXHheJ4YmOw5FG4",
    worksheet_title="Survey Results",          # имя вкладки, которую ты смотришь
    # worksheet_gid=0,                          # либо так — по gid, если знаешь
    scopes=Settings.SCOPES,
    token_path=Settings.GOOGLE_AUTH_TOKEN_PATH,
    secret_path=Settings.GOOGLE_CLIENT_SECRET_PATH,
)

# helpers
def _col(n: int) -> str:
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

LAST_COL = _col(len(HEADERS))  # напр., 'U' если колонок 21
HEADER_RANGE = f"A1:{LAST_COL}1"

async def ensure_header_async(ws) -> None:
    # кладём шапку ровно в A1:{LAST_COL}1
    cur = await asyncio.to_thread(ws.get_all_values)
    if not cur or cur[0][:len(HEADERS)] != HEADERS:
        await asyncio.to_thread(
            ws.update,
            HEADER_RANGE,
            [HEADERS],
            value_input_option="USER_ENTERED",
        )

async def save_survey(*, data: dict, user_id: int, username: str | None, ws=SHEET) -> None:
    await ensure_header_async(ws)

    row = [
        datetime.now().isoformat(timespec="seconds"),
        str(user_id),
        username or "",
        data.get("q1_bought_art",""),
        data.get("q2_expertise",""),
        _join(data.get("q3_difficulties")),
        _join(data.get("q4_goal")),
        _join(data.get("q4_what_to_search")),
        _join(data.get("q5_colors")),
        data.get("q6_favorite_authors",""),
        data.get("q7_folder_link",""),
        data.get("q8_mood",""),
        data.get("q9_wishes",""),
        _join(data.get("q10_size")),
        _join(data.get("q11_format")),
        data.get("q12_folder_link",""),
        data.get("q13_budget",""),
        data.get("q14_delivery_country",""),
        _join(data.get("q15_hobbies")),
        data.get("q16_contact_method",""),
        data.get("q17_contact_details",""),
    ]
    # выравниваем длину ровно под шапку
    if len(row) < len(HEADERS):
        row += [""] * (len(HEADERS) - len(row))
    elif len(row) > len(HEADERS):
        row = row[:len(HEADERS)]

    # вычисляем следующий ряд (надёжно для небольших объёмов)
    used = await asyncio.to_thread(ws.get_all_values)
    next_r = len(used) + 1            # после заголовка и данных
    rng = f"A{next_r}:{LAST_COL}{next_r}"

    backoff = 0.5
    for attempt in range(4):
        try:
            await asyncio.to_thread(
                ws.update,
                rng,
                [row],
                value_input_option="USER_ENTERED",
            )
            return
        except APIError as e:
            s = str(e)
            transient = any(x in s for x in ("rateLimitExceeded","internalError","backendError","quotaExceeded","503","500"))
            if attempt < 3 and transient:
                await asyncio.sleep(backoff); backoff *= 2
                continue
            raise
