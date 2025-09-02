from collections import defaultdict
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from keyboards.user import survey_button, q5_done_kb, q5_toggle_kb, multi_choice_kb
from aiogram.enums.parse_mode import ParseMode
from states.states import SurveyStates
from settings import Settings, SHEET
import asyncio
from routers import user_form
from utils.sheets import save_survey
from utils.helpers import format_survey_for_sheets, fetch_photo_bytes_verbose
from utils.localization import localize_options, kb_texts, question_text
import logging
from aiogram.types.error_event import ErrorEvent


user_router = Router()


@user_router.callback_query(F.data == "skip")
async def skip_question_cb(cq: CallbackQuery, state: FSMContext):
    cur = await state.get_state()
    for st, (field, default, next_func) in user_form.PASS_MAP.items():
        if cur == st.state:
            data = await state.get_data()
            data[field] = default
            await state.set_data(data)

            try:
                await cq.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass

            await cq.answer("Пропущено.")
            await next_func(cq.message, state)
            return

    await cq.answer("Этот шаг нельзя пропустить", show_alert=True)



@user_router.callback_query(F.data.startswith("back:"))
async def go_back(cq: CallbackQuery, state: FSMContext):
    key = cq.data.split(":", 1)[1]
    print(key, cq.data)
    pair = user_form.back_map.get(key)
    if not pair:
        await cq.answer("Назад сюда нельзя", show_alert=True)
        return
    new_state, ask_func = pair

    data = await state.get_data()
    if key in data:
        data.pop(key)
    await state.set_data(data)

    await cq.answer()
    try:
        await cq.message.delete()
    except Exception:
        pass
    await state.set_state(new_state)
    await ask_func(cq.message, state)


@user_router.message(CommandStart())
async def start_message(m: Message):
    button = await survey_button()
    await m.answer(text = (
                        "<b>Настоящее искусство</b> – это погружение в чувства, эмоции и воспоминания. "
                        "Но самостоятельно выбрать что-то для своего дома бывает очень сложно и требует много времени.\n\n"
                        "Мы создали <b>Arterier</b>, чтобы Вы могли создать свой мир чувств и ощущений с помощью "
                        "настоящих произведений искусства в вашем доме. "
                        "Расскажите свою историю, и мы подберем для Вас работы, которые подчеркнут "
                        "индивидуальность вашего пространства."
                        "Мы работаем в команде с <b>профессиональными галеристами</b>, дизайнерами интерьеров "
                        "и привлекаем <b>искусственный интеллект</b>, чтобы помочь вам сделать выбор из сотен вариантов.\n\n"
                        "<b>Как это работает:</b>\n\n"
                        "1️⃣ Заполните анкету, и мы подберем для вас подходящие варианты в местных галереях "
                        "для уточнения направлений и пожеланий.\n\n"
                        "2️⃣ Мы делаем три итерации, чтобы приблизиться к вашим ожиданиям.\n\n"
                        "3️⃣ Вы можете самостоятельно заказать выбранный предмет искусства "
                        "или обратиться к нам за организацией примерки и покупки.\n\n"
                        "<i>Arterier – Ваш куратор в мире искусства</i>\n"
                        "<i>и это сообщение тоже</i>"), 
                    parse_mode=ParseMode("HTML"))
    await m.answer("Для того чтобы начать опрос выберите язык.", reply_markup=button)
    

@user_router.callback_query((F.data == "lang:ru") | (F.data == "lang:en"))
async def start_survey_handl(cq: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        lang = cq.data[5:] if cq.data and cq.data.startswith("lang:") else None
        if lang not in {"ru", "en"}:
            await cq.answer("Некорректный выбор языка.", show_alert=True)
            return
        await state.update_data(lang=lang)
        await cq.answer()
        try:
            await cq.message.edit_reply_markup()
        except Exception:
            pass
        await user_form.FormQuestions.ask_q1(cq.message, state)
    except Exception as e:
        await cq.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.callback_query(SurveyStates.q1_bought_art)
async def q1_bought_art_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = (cq.data or "").strip()
        if not value:
            await cq.answer("Empty selection. Click one of the buttons.", show_alert=True)
            return
        await cq.answer() 
        await cq.message.edit_reply_markup()
        if value == "other":
            await user_form.FormQuestions.ask_q1_other(cq.message, state)
        else:
            await state.update_data(q1_bought_art=value)
            await user_form.FormQuestions.ask_q2(cq.message, state)
    except Exception:
        await cq.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q1_bought_art_other)
async def q1_other_art_other_handl(message: Message, state: FSMContext):
    try:
        await state.update_data(q1_bought_art=message.text)
        await user_form.FormQuestions.ask_q2(message, state)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.callback_query(SurveyStates.q2_expertise)
async def q2_expertise_handl(cq: CallbackQuery, state: FSMContext):
    try:
        await cq.message.edit_reply_markup()
        await state.update_data(q2_expertise=cq.data)
        await user_form.FormQuestions.ask_q3(cq.message, state)
    except Exception:
        await cq.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.callback_query(SurveyStates.q3_difficulties)
async def q3_difficulties_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = cq.data 
        data = await state.get_data()
        selected = set(data.get("q3_difficulties", []))
        if value == "done":
            if selected:
                await state.update_data(q3_difficulties=list(selected))
                await cq.message.edit_reply_markup()
                await user_form.FormQuestions.ask_q4_goal(cq.message, state)
                return
            else:
                await cq.answer("Выберите хотя бы один вариант или «Другое»", show_alert=True)
                return
            
        if value == "other":
            await cq.message.edit_reply_markup()
            await state.update_data(q3_difficulties=list(selected))
            await user_form.FormQuestions.ask_q3_other(cq.message, state)
            return
        
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)
        data = await state.get_data()
        lang = data["lang"]
        opts = localize_options(lang=lang, group_key="q3_options")
        buttons = kb_texts(lang=lang)
        kb = await multi_choice_kb(selected=selected, options=opts, rows=[1, 1, 1, 1, 1, 2], back_value="q2_expertise", back_text=buttons["back"], done_text=buttons["done"])
        await state.update_data(q3_difficulties=list(selected))
        await cq.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        await cq.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.message(SurveyStates.q3_difficulties_other)
async def q3_difficulties_other_text(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        selected = set(data.get("q3_difficulties", []))
        selected.add(f"other:{message.text.strip()}")
        await state.update_data(q3_difficulties=list(selected))
        await user_form.FormQuestions.ask_q4_goal(message, state)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)



@user_router.callback_query(SurveyStates.q4_goal)
async def q4_goal_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = cq.data
        data = await state.get_data()
        selected = set(data.get("q4_goal", []))
        if value == "done":
            if selected:
                await state.update_data(q4_goal=list(selected))
                await cq.message.edit_reply_markup()
                await user_form.FormQuestions.ask_q4(cq.message, state)
                return
            else:
                await cq.answer("Выберите хотя бы один вариант или «Другое»", show_alert=True)
                return


        if value == "other":
            await cq.message.edit_reply_markup()
            await state.update_data(q4_goal=list(selected))
            await user_form.FormQuestions.ask_q4_goal_other(cq.message, state)
            return
        
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)
        data = await state.get_data()
        lang = data["lang"]
        opts = localize_options(lang=lang, group_key="q4_goal_options")
        buttons = kb_texts(lang=lang)
        kb = await multi_choice_kb(selected=selected, options=opts, rows=[1, 1, 1, 2], back_value="q3_difficults", back_text=buttons["back"], done_text=buttons["done"])
        await state.update_data(q4_goal=list(selected))
        await cq.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        await cq.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q4_goal_other)
async def q4_goal_other_handl(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        selected = set(data.get("q4_goal", []))
        selected.add(f"other:{message.text.strip()}")
        await state.update_data(q4_goal=list(selected))
        await user_form.FormQuestions.ask_q4(message, state)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.callback_query(SurveyStates.q4_what_to_search)
async def q4_what_to_search_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = cq.data
        data = await state.get_data()
        selected = set(data.get("q4_what_to_search", []))
        if value == "done":
            if selected:
                await state.update_data(q4_what_to_search=list(selected))
                await cq.message.edit_reply_markup()
                await user_form.FormQuestions.ask_q5(cq.message, state)
                return
            else:
                await cq.answer("Выберите хотя бы один вариант или «Другое»", show_alert=True)
                return

        if value == "other":
            await cq.message.edit_reply_markup()
            await state.update_data(q3_difficulties=list(selected))
            await user_form.FormQuestions.ask_q3_other(cq.message, state)
            return
        
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)
        await state.update_data(q4_what_to_search=list(selected))
        data = await state.get_data()
        lang = data["lang"]
        opts = localize_options(lang=lang, group_key="q4_options")
        buttons = kb_texts(lang=lang)
        kb = await multi_choice_kb(selected=selected, options=opts, back_value="q4_goal", rows=[2,2,2,2], back_text=buttons["back"], done_text=buttons["done"])
        await cq.message.edit_reply_markup(reply_markup=kb)
        await cq.answer()
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)




async def ask_q5(message: Message, state: FSMContext):
    try:
        await state.update_data(q5_colors=[])
        msg_ids: dict[str, int] = {}

        selected = set()
        data = await state.get_data()
        lang = data["lang"]
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q5_options")
        for key, title in opts:
            photo = FSInputFile(str(Settings.Q5_IMAGES[key]))
            msg = await message.answer_photo(
                photo=photo,
                caption=title,
                reply_markup=q5_toggle_kb(key, selected, select_text=buttons["select"])
            )
            msg_ids[key] = msg.message_id
        if lang == "ru":   
            done_answer_text = "Когда определитесь, нажмите «Готово»."
        else:
            done_answer_text = "Once you have decided, click «Done»."
        await message.answer(
            text = done_answer_text,
            reply_markup=q5_done_kb(back_value="q4_what_to_search", done_text=buttons["done"], back_text=buttons["back"])
        )

        await state.set_state(SurveyStates.q5_colors)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)




@user_router.callback_query(SurveyStates.q5_colors, F.data.startswith("q5:toggle:"))
async def q5_toggle_handl(cq: CallbackQuery, state: FSMContext):
    try:
        await cq.answer()
        _, _, key = cq.data.split(":", 2)  

        data = await state.get_data()
        selected = set(data.get("q5_colors", []))
        msg_ids: dict = data.get("q5_msg_ids", {})

        selected.remove(key) if key in selected else selected.add(key)
        await state.update_data(q5_colors=list(selected))
        data = await state.get_data()
        lang = data["lang"]
        buttons = kb_texts(lang=lang)
        await cq.bot.edit_message_reply_markup(
            chat_id=cq.message.chat.id,
            message_id=msg_ids.get(key, cq.message.message_id),
            reply_markup=q5_toggle_kb(key, selected, select_text=buttons["select"])
        )
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.callback_query(SurveyStates.q5_colors, F.data == "q5:done")
async def q5_done_handl(cq: CallbackQuery, state: FSMContext):
    try:
        await cq.answer()
        data = await state.get_data()
        selected = data.get("q5_colors", [])
        if not selected:
            await cq.answer("Выберите хотя бы один вариант", show_alert=True)
            return

        await state.update_data(q5_colors=selected)
        msg_ids: dict = data.get("q5_msg_ids", {})
        await cq.bot.edit_message_reply_markup(
            chat_id=cq.message.chat.id,
            message_id=msg_ids.get("_done", cq.message.message_id),
            reply_markup=None
        )

        await user_form.FormQuestions.ask_q6(cq.message, state)
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q6_favorite_authors)
async def q6_favorite_authors_handl(m: Message, state: FSMContext):
    try:
        await state.update_data(q6_favorite_authors=m.text)
        await user_form.FormQuestions.ask_q7(m, state)
    except Exception:
        await m.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


q7_media_groups = defaultdict(list)

@user_router.message(SurveyStates.q7_references, F.media_group_id)
async def handle_album_part(message: Message, state: FSMContext):
    gid = message.media_group_id
    q7_media_groups[gid].append(message)

    await asyncio.sleep(0.5)

    if q7_media_groups.get(gid):
        msgs = q7_media_groups.pop(gid)
        await process_q7(msgs, state, tail=message)


@user_router.message(SurveyStates.q7_references, (F.photo | F.document))
async def handle_single(message: Message, state: FSMContext):
    await process_q7([message], state, tail=message)


async def process_q7(messages: list[Message], state: FSMContext, tail: Message):
    try: 
        data = await state.get_data()
        files: list = data.get("q7_references", [])

        for m in messages:
            if len(files) >= Settings.MAX_FILES:
                break
            if m.photo:
                p = m.photo[-1]
                files.append({"kind": "photo", "file_id": p.file_id})
            elif m.document:
                d = m.document
                files.append({"kind": "document", "file_id": d.file_id, "name": d.file_name})

        await state.update_data(q7_references=files)

        if len(files) <= Settings.MAX_FILES:
            await user_form.FormQuestions.ask_q8(tail, state)
        else:
            await tail.answer(f"Вы добавили больше 5 фото, пожалуйста прикрепите не более 5 фотографий или нажмите кнопку пропустить.")
    except Exception:
        await tail.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q8_mood)
async def q8_mood_handl(m: Message, state: FSMContext):
    try:
        await state.update_data(q8_mood=m.text)
        await user_form.FormQuestions.ask_q9(m, state)
    except Exception:
        await m.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.message(SurveyStates.q9_wishes)
async def q9_wishes_handl(m: Message, state: FSMContext):
    try:
        await state.update_data(q9_wishes=m.text)
        await user_form.FormQuestions.ask_q10(m, state)
    except Exception:
        await m.answer("Something went wrong, restart the survey or click back button.", show_alert=True)



@user_router.callback_query(SurveyStates.q10_size)
async def q10_size_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = cq.data
        data = await state.get_data()
        selected = set(data.get("q10_size", []))
        if value == "done":
            if selected:
                await state.update_data(q10_size=list(selected))
                await cq.message.edit_reply_markup()
                await user_form.FormQuestions.ask_q11(cq.message, state)
                return
            else:
                await cq.answer("Выберите хотя бы один вариант или «Другое»", show_alert=True)
                return
            
        if value == "other":
            await cq.message.edit_reply_markup()
            await state.update_data(q10_size=list(selected))
            await user_form.FormQuestions.ask_q10_other(cq.message, state)
            return
        
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)

        await state.update_data(q10_size=list(selected))
        data = await state.get_data()
        lang = data["lang"]
        opts = localize_options(lang=lang, group_key="q10_options")
        buttons = kb_texts(lang)
        kb = await multi_choice_kb(selected=selected, options=opts, back_value="q9_wishes", rows=[2, 2, 2, 2 ,1, 2], back_text=buttons["back"], done_text=buttons["done"])
        await cq.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.message(SurveyStates.q10_size_other)
async def q10_size_other_text(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        selected = set(data.get("q10_size", []))
        selected.add(f"other:{message.text.strip()}")
        await state.update_data(q10_size=list(selected))
        await user_form.FormQuestions.ask_q11(message, state)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.callback_query(SurveyStates.q11_format)
async def q11_format_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = cq.data
        data = await state.get_data()
        selected = set(data.get("q11_format", []))
        if value == "done":
            if selected:
                await state.update_data(q11_format=list(selected))
                await cq.message.edit_reply_markup()
                await user_form.FormQuestions.ask_q12(cq.message, state)
                return
            else:
                await cq.answer("Выберите хотя бы один вариант или «Другое»", show_alert=True)
                return
            
        if value == "other":
            await cq.message.edit_reply_markup()
            await state.update_data(q11_format=list(selected))
            await user_form.FormQuestions.ask_q11_other(cq.message, state)
            return
        
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)

        await state.update_data(q11_format=list(selected))
        data = await state.get_data()
        lang = data["lang"]
        opts = localize_options(lang=lang, group_key="q11_options")
        buttons = kb_texts(lang)
        kb = await multi_choice_kb(selected=selected, options=opts, back_value="q10_size", rows=[2, 2, 1, 2], back_text=buttons["back"], done_text=buttons["done"])
        await cq.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.message(SurveyStates.q11_format_other)
async def q11_format_other_text(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        selected = set(data.get("q11_format", []))
        selected.add(f"other:{message.text.strip()}")
        await state.update_data(q11_format=list(selected))
        await user_form.FormQuestions.ask_q12(message, state)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


q12_media_groups = defaultdict(list)

@user_router.message(SurveyStates.q12_interior_photos, F.media_group_id)
async def handle_album_part(message: Message, state: FSMContext):
    gid = message.media_group_id
    q12_media_groups[gid].append(message)

    await asyncio.sleep(0.5)

    if q12_media_groups.get(gid):
        msgs = q12_media_groups.pop(gid)
        await process_q12(msgs, state, tail=message)


@user_router.message(SurveyStates.q12_interior_photos, (F.photo | F.document))
async def handle_single(message: Message, state: FSMContext):
    await process_q12([message], state, tail=message)


async def process_q12(messages: list[Message], state: FSMContext, tail: Message):
    try: 
        data = await state.get_data()
        files: list = data.get("q12_interior_photos", [])

        for m in messages:
            if len(files) >= Settings.MAX_FILES:
                break
            if m.photo:
                p = m.photo[-1]
                files.append({"kind": "photo", "file_id": p.file_id})
            elif m.document:
                d = m.document
                files.append({"kind": "document", "file_id": d.file_id, "name": d.file_name})

        await state.update_data(q12_interior_photos=files)

        if len(files) <= Settings.MAX_FILES:
            await user_form.FormQuestions.ask_q13(tail, state)
        else:
            await tail.answer(f"Вы добавили больше 5 фото, пожалуйста прикрепите не более 5 фотографий или нажмите кнопку пропустить.")
    except Exception:
        await tail.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.callback_query(SurveyStates.q13_budget)
async def q13_budget_handl(cq: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(q13_budget=cq.data)
        await cq.message.edit_reply_markup()
        await user_form.FormQuestions.ask_q14(cq.message, state)
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q14_delivery_country)
async def q14_delivery_country_handl(m: Message, state: FSMContext):
    try:
        await state.update_data(q14_delivery_country=m.text)
        await user_form.FormQuestions.ask_q15(m, state)
    except Exception:
        await m.answer("Something went wrong, restart the survey or click back button.", show_alert=True)



@user_router.callback_query(SurveyStates.q15_hobbies)
async def q15_hobbies_handl(cq: CallbackQuery, state: FSMContext):
    try:
        value = cq.data 
        data = await state.get_data()
        selected = set(data.get("q15_hobbies", []))
        if value == "done":
            if selected:
                await state.update_data(q15_hobbies=list(selected))
                await cq.message.edit_reply_markup()
                await user_form.FormQuestions.ask_q16(cq.message, state)
                return
            else:
                await cq.answer("Выберите хотя бы один вариант или «Другое»", show_alert=True)
                return
            
        if value == "other":
            await cq.message.edit_reply_markup()
            await state.update_data(q15_hobbies=list(selected))
            await user_form.FormQuestions.ask_q15_other(cq.message, state)
            return
        
        if value in selected:
            selected.remove(value)
        else:
            selected.add(value)

        await state.update_data(q15_hobbies=list(selected))
        data = await state.get_data()
        lang = data["lang"]
        opts = localize_options(lang=lang, group_key="q15_options")
        buttons = kb_texts(lang)
        kb = await multi_choice_kb(selected=selected, options=opts, back_value="q14_delivery_country", rows=[1,1,1,1,1,1,1,1,2,2,2],  back_text=buttons["back"], done_text=buttons["done"])
        await cq.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q15_hobbies_other)
async def q15_format_other_text(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        selected = set(data.get("q15_hobbies", []))
        selected.add(f"other:{message.text.strip()}")
        await state.update_data(q15_hobbies=list(selected))
        await user_form.FormQuestions.ask_q16(message, state)
    except Exception:
        await message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)


@user_router.callback_query(SurveyStates.q16_contact_method)
async def q16_contact_method_handl(cq: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(q16_contact_method=cq.data)
        await cq.message.edit_reply_markup()
        await user_form.FormQuestions.ask_q17(cq.message, state)
    except Exception:
        await cq.message.answer("Something went wrong, restart the survey or click back button.", show_alert=True)

@user_router.message(SurveyStates.q17_contact_details)
async def q17_contact_details_handl(message: Message, state: FSMContext):
    await state.update_data(q17_contact_details=message.text)
    snapshot = await state.get_data()  # снимок данных на сейчас

    await message.answer(
        "Спасибо! Мы вернемся с тремя вариантами для обратной связи в течение 72 часов. "
        "В рамках бесплатного теста мы предлагаем 5 работ различных художников."
    )

    async def bg_finalize():
        try:
            q12_ids = [x["file_id"] for x in snapshot.get("q12_interior_photos", []) if isinstance(x, dict) and x.get("file_id")]
            q7_ids  = [x["file_id"] for x in snapshot.get("q7_references", [])        if isinstance(x, dict) and x.get("file_id")]

            async def up_q7(fid: str):
                return await fetch_photo_bytes_verbose(
                    file_id=fid, bot=message.bot, user_id=message.from_user.id,
                    folder_id=Settings.DRIVE_FOLDER_Q7, file_name="q7_reference"
                )

            async def up_q12(fid: str):
                return await fetch_photo_bytes_verbose(
                    file_id=fid, bot=message.bot, user_id=message.from_user.id,
                    folder_id=Settings.DRIVE_FOLDER_Q12, file_name="q12_interier"
                )

            q7_res  = await asyncio.gather(*(up_q7(i)  for i in q7_ids),  return_exceptions=True)
            q12_res = await asyncio.gather(*(up_q12(i) for i in q12_ids), return_exceptions=True)

            def first_link(lst):
                for r in lst:
                    if isinstance(r, str) and r:
                        return r
                return ""

            q7_link  = first_link(q7_res)
            q12_link = first_link(q12_res)
            await state.update_data(q7_folder_link=q7_link, q12_folder_link=q12_link)
            data_for_sheet = format_survey_for_sheets(data=await state.get_data())

            await save_survey(
                SHEET,
                data=data_for_sheet,
                user_id=message.from_user.id,
                username=message.from_user.username,
            )
        except Exception:
            logging.exception("Finalize submission failed")

    asyncio.create_task(bg_finalize())

        

