# ask_questions.py
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.states import SurveyStates
from utils.localization import localize_options, kb_texts, question_text
from keyboards.user import one_choice_kb, multi_choice_kb, back_button
from settings import Settings


class FormQuestions:
    # === 1 ===
    async def ask_q1(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q1.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q1_options")
        await message.answer(
            text,
            reply_markup=await one_choice_kb(
                options=opts,
                back_value=None,
                cols=2,
                back_text=buttons["back"]
            )
        )
        await state.set_state(SurveyStates.q1_bought_art)

   
    async def ask_q1_other(message: Message, state: FSMContext):
        await message.answer("Напишите свой вариант 👇")
        await state.set_state(SurveyStates.q1_bought_art_other)


    # === 2 ===
    async def ask_q2(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q2.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q2_options")
        await message.answer(
            text,
            reply_markup=await one_choice_kb(
                opts,
                rows=[2, 2, 1, 1],
                back_value="q1_bought_art",
                back_text=buttons["back"]
            )
        )
        await state.set_state(SurveyStates.q2_expertise)


    # === 3 === (мультивыбор + «Другое»)
    async def ask_q3(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q3.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q3_options")
        await message.answer(
            text=text,
            reply_markup=await multi_choice_kb(
                options=opts,
                selected=set(),
                rows=[1, 1, 1, 1, 1, 2],
                back_text=buttons["back"],        
                back_value="q2_expertise",
                done_text=buttons["done"]
            )
        )
        await state.set_state(SurveyStates.q3_difficulties)

    async def ask_q3_other(message: Message, state: FSMContext):
        await message.answer("Опишите вашу сложность/вариант 👇")
        await state.set_state(SurveyStates.q3_difficulties_other)

    async def ask_q4_goal(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q4_goal.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q4_goal_options")
        await message.answer(
            text=text,
            reply_markup=await multi_choice_kb(
                options=opts,
                selected=set(),
                rows=[1,1,1,2],
                back_value="q3_difficulties",
                back_text=buttons["back"],
                done_text=buttons["done"]
            )
        )
        await state.set_state(SurveyStates.q4_goal)

    async def ask_q4_goal_other(message: Message, state: FSMContext):
        await message.answer("Опишите свой вариант 👇")
        await state.set_state(SurveyStates.q4_goal_other)

    # === 4 === (мультивыбор)
    async def ask_q4(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q4.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q4_options")
        print(opts)
        await message.answer(
            text=text,
            reply_markup=await multi_choice_kb(
                options=opts,
                selected=set(),
                rows=[2,2,2,2],
                back_value="q4_goal",
                back_text=buttons["back"],
                done_text=buttons["done"]
            )
        )
        await state.set_state(SurveyStates.q4_what_to_search)

    # === 5 === 
    async def ask_q5(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q5.text")
        await message.answer(text=text)
        from routers.user import ask_q5 as show_q5_cards 
        await show_q5_cards(message, state)                


    # === 6 === (текст)
    async def ask_q6(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q6.text")
        buttons = kb_texts(lang=lang)
        await message.answer(
            text=text,
            reply_markup= await back_button(back_value="q5_colors", skip_text=buttons["skip"], back_text=buttons["back"], can_pass=True)
        )
        await state.set_state(SurveyStates.q6_favorite_authors)


    # === 7 === (файлы референсов)
    async def ask_q7(message: Message, state: FSMContext):
        await state.update_data(q7_files=[], q7_done=False)
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q7.text")
        buttons = kb_texts(lang=lang)
        await message.answer(
            text=text, 
            reply_markup= await back_button(back_value="q6_favorite_authors", can_pass=True, skip_text=buttons["skip"], back_text=buttons["back"])
        )
        await state.set_state(SurveyStates.q7_references)


    # === 8 === (текст)
    async def ask_q8(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q8.text")
        buttons = kb_texts(lang=lang)
        await message.answer(text=text,
                reply_markup= await back_button(back_value="q7_references", back_text=buttons["back"])
                )
        
        await state.set_state(SurveyStates.q8_mood)


    # === 9 === (текст)
    async def ask_q9(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q9.text")
        buttons = kb_texts(lang=lang)
        await message.answer(text=text,
                             reply_markup= await back_button(back_value="q8_mood", back_text=buttons["back"]))
        await state.set_state(SurveyStates.q9_wishes)


    # === 10 === (мультивыбор + «Другое») — Размер пространства
    async def ask_q10(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q10.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q10_options")
        await message.answer(
            text=text,
            reply_markup=await multi_choice_kb(
                options=opts,
                selected=set(),
                rows=[2, 2, 2, 2 ,1, 2],
                back_value="q9_wishes",
                back_text=buttons["back"],
                done_text=buttons["done"]
            )
        )
        await state.set_state(SurveyStates.q10_size)

    async def ask_q10_other(message: Message, state: FSMContext):
        await message.answer("Напишите свой размер/формулировку 👇")
        await state.set_state(SurveyStates.q10_size_other)


    # === 11 === (мультивыбор + «Другое») — Формат
    async def ask_q11(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q11.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q11_options")
        await message.answer(
            text=text,
            reply_markup=await multi_choice_kb(
                options=opts,
                selected=set(),
                rows = [2,2,1,2],
                back_value="q10_size",
                back_text=buttons["back"],
                done_text=buttons["done"]
            )
        )
        await state.set_state(SurveyStates.q11_format)

    async def ask_q11_other(message: Message, state: FSMContext):
        await message.answer("Опишите желаемый формат 👇")
        await state.set_state(SurveyStates.q11_format_other)


    # === 12 === (фото интерьера) — файлы
    async def ask_q12(message: Message, state: FSMContext):
        await state.update_data(q12_files=[], q12_done=False)
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q12.text")
        buttons = kb_texts(lang=lang)
        await message.answer(
            text=text, 
            reply_markup= await back_button(back_value="ask_q11",can_pass=True, back_text=buttons["back"], skip_text=buttons["skip"])
        )
        await state.set_state(SurveyStates.q12_interior_photos)


    # === 13 === (одиночный выбор — бюджет)
    async def ask_q13(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q13.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q13_options")
        await message.answer(
            text=text,
            reply_markup=await one_choice_kb(
                options=opts,
                back_value="q12_interior_photos", back_text=buttons["back"], rows=[2,2,1,1]
            )
        )
        await state.set_state(SurveyStates.q13_budget)


    # === 14 === (одиночный выбор/текст — страна)
    async def ask_q14(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q14.text")
        buttons = kb_texts(lang=lang)
        await message.answer(text=text, 
                             reply_markup= await back_button(back_value="q13_budget", back_text=buttons["back"]))
        await state.set_state(SurveyStates.q14_delivery_country)


    # === 15 === (мультивыбор + «Другое») — Хобби
    async def ask_q15(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q15.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q15_options")
        await message.answer(
            text=text,
            reply_markup=await multi_choice_kb(
                options=opts,
                selected=set(),
                back_value="q14_delivery_country", 
                back_text=buttons["back"], 
                done_text=buttons["done"], 
                rows = [1,1,1,1,1,1,1,1,2,2,1,2],
            )
        )
        await state.set_state(SurveyStates.q15_hobbies)

    async def ask_q15_other(message: Message, state: FSMContext):
        await message.answer("Опишите «другое» хобби 👇")
        await state.set_state(SurveyStates.q15_hobbies_other)


    # === 16 === (одиночный выбор) — способ связи
    async def ask_q16(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q16.text")
        buttons = kb_texts(lang=lang)
        opts = localize_options(lang=lang, group_key="q16_options")
        await message.answer(
            text=text,
            reply_markup=await one_choice_kb(
                options=opts, 
                back_value="q15_hobbies",
                back_text=buttons["back"]
            )
        )
        await state.set_state(SurveyStates.q16_contact_method)


    # === 17 === (текст) — контакт
    async def ask_q17(message: Message, state: FSMContext):
        data = await state.get_data()
        lang = data["lang"]
        text = question_text(lang=lang, key="q17.text")
        buttons = kb_texts(lang=lang)
        await message.answer(text=text,
                             reply_markup= await back_button(back_value="q16_contact_method", back_text=buttons["back"]))
        await state.set_state(SurveyStates.q17_contact_details)


    # === Завершение
    async def ask_finished(message: Message, state: FSMContext):
        await message.answer("Спасибо! Анкета заполнена. Мы вернёмся к вам с подборкой 🙌")
        await state.set_state(SurveyStates.finished)


back_map = {
    "q1_bought_art": (SurveyStates.q1_bought_art, FormQuestions.ask_q1),
    "q1_bought_art_other": (SurveyStates.q1_bought_art_other, FormQuestions.ask_q1_other),
    "q2_expertise": (SurveyStates.q2_expertise, FormQuestions.ask_q2),
    "q3_difficulties": (SurveyStates.q3_difficulties, FormQuestions.ask_q3),
    "q3_difficulties_other": (SurveyStates.q3_difficulties_other, FormQuestions.ask_q3_other),
    "q4_goal": (SurveyStates.q4_goal, FormQuestions.ask_q4_goal),
    "q4_goal_other": (SurveyStates.q4_goal_other, FormQuestions.ask_q4_goal_other),
    "q4_what_to_search": (SurveyStates.q4_what_to_search, FormQuestions.ask_q4),
    "q5_colors": (SurveyStates.q5_colors, FormQuestions.ask_q5),
    "q6_favorite_authors": (SurveyStates.q6_favorite_authors, FormQuestions.ask_q6),
    "q7_references": (SurveyStates.q7_references, FormQuestions.ask_q7),
    "q8_mood": (SurveyStates.q8_mood, FormQuestions.ask_q8),
    "q9_wishes": (SurveyStates.q9_wishes, FormQuestions.ask_q9),
    "q10_size": (SurveyStates.q10_size, FormQuestions.ask_q10),
    "q10_size_other": (SurveyStates.q10_size_other, FormQuestions.ask_q10_other),
    "q11_format": (SurveyStates.q11_format, FormQuestions.ask_q11),
    "q11_format_other": (SurveyStates.q11_format_other, FormQuestions.ask_q11_other),
    "q12_interior_photos": (SurveyStates.q12_interior_photos, FormQuestions.ask_q12),
    "q13_budget": (SurveyStates.q13_budget, FormQuestions.ask_q13),
    "q14_delivery_country": (SurveyStates.q14_delivery_country, FormQuestions.ask_q14),
    "q15_hobbies": (SurveyStates.q15_hobbies, FormQuestions.ask_q15),
    "q15_hobbies_other": (SurveyStates.q15_hobbies_other, FormQuestions.ask_q15_other),
    "q16_contact_method": (SurveyStates.q16_contact_method, FormQuestions.ask_q16),
    "q17_contact_details": (SurveyStates.q17_contact_details, FormQuestions.ask_q17),
    "finished": (SurveyStates.finished, FormQuestions.ask_finished),
    }

PASS_MAP = {
    SurveyStates.q6_favorite_authors:  ("q6_favorite_authors", "",   FormQuestions.ask_q7),
    SurveyStates.q7_references:        ("q7_references",      [],    FormQuestions.ask_q8),
    SurveyStates.q12_interior_photos:  ("q12_interior_photos",[],    FormQuestions.ask_q13),
}