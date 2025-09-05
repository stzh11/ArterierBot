
from settings import Settings
DEFAULT_LANG = "ru"


def norm_lang(code: str | None) -> str:
    if not code:
        return DEFAULT_LANG
    code = code.lower()
    if code.startswith("ru"):
        return "ru"
    return "en"


def question_text(lang: str, key: str,) -> str:
    lang = norm_lang(lang)
    text = Settings.LOCALES.get(lang, {}).get(key) or Settings.LOCALES[DEFAULT_LANG].get(key)
    return text



def localize_options(lang: str, group_key: str) -> list[tuple[str, str]]:
    lang = norm_lang(lang)
    options_dict = Settings.LOCALES.get(lang, {}).get(group_key) or Settings.LOCALES[DEFAULT_LANG].get(group_key) 
    return list(options_dict.items())


def kb_texts(lang: str) -> dict[str, str]:
    lang = norm_lang(lang)
    return {
        "done": Settings.LOCALES.get(lang, {}).get("buttons.done") or Settings.LOCALES[DEFAULT_LANG].get("buttons.done"),
        "back": Settings.LOCALES.get(lang, {}).get("buttons.back") or Settings.LOCALES[DEFAULT_LANG].get("buttons.back"),
        "skip": Settings.LOCALES.get(lang, {}).get("buttons.skip") or Settings.LOCALES[DEFAULT_LANG].get("buttons.skip"),
        "select": Settings.LOCALES.get(lang, {}).get("buttons.select") or Settings.LOCALES[DEFAULT_LANG].get("buttons.select"),
    }
