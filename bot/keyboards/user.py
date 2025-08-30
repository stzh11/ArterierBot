from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional, Sequence


async def survey_button() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text="🇷🇺 Русский", callback_data="lang:ru")
    kb.button(text="🇬🇧 English", callback_data="lang:en")
    return kb.as_markup()



async def one_choice_kb(options: set,
                        back_value: str = None, 
                        back_text: str = "",
                        rows: Optional[Sequence[int]] = None,
                        cols: Optional[int] = None, ) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for key, value in options:
        kb.button(text=value, callback_data=key)
    
    if back_value:
        kb.button(text="◀️ " + back_text, callback_data=f"back:{back_value}")

    if rows:
        kb.adjust(*rows)
    elif cols:
        kb.adjust(cols, repeat=True)
    else:
        kb.adjust(1, repeat=True)  

    return kb.as_markup() 



async def multi_choice_kb(options: set, 
                          selected: set[str] = None,
                          rows: Optional[Sequence[int]] = None,
                          cols: Optional[int] = None, 
                          back_value: str = None,
                          back_text: str = "", 
                          done_text: str = "") -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    selected = selected or set()

    for value, text in options:
        check = "☑️" if value in selected else "⬜️"
        kb.button(text=f"{check} {text}", callback_data=f"{value}")

    if back_value:
        kb.button(text="◀️ " + back_text, callback_data=f"back:{back_value}")

    kb.button(text=f"✅ {done_text}", callback_data="done")

    if rows:
        kb.adjust(*rows)
    elif cols:
        kb.adjust(cols, repeat=True)
    else:
        kb.adjust(1, repeat=True)  

    return kb.as_markup()



def q5_toggle_kb(key: str, selected: set[str], select_text: str = "") -> InlineKeyboardBuilder:
    check = "☑️" if key in selected else "⬜️"
    kb = InlineKeyboardBuilder()
    kb.button(text=f"{check} {select_text}", callback_data=f"q5:toggle:{key}")
    return kb.as_markup()

def q5_done_kb(back_value: str = None, back_text: str = "", done_text: str = "") -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ "+done_text, callback_data="q5:done")
    if back_value:
        kb.button(text="◀️ "+back_text, callback_data=f"back:{back_value}")
    return kb.as_markup()



async def back_button(back_value: str = None, back_text: str = "", skip_text:str = "",can_pass: bool = False) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"◀️ {back_text}", callback_data=f"back:{back_value}")
    if can_pass:
        kb.adjust(2)
        kb.button(text="⏭ "+skip_text, callback_data="skip")
    
    return kb.as_markup()
