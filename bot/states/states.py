from aiogram.fsm.state import StatesGroup, State

class SurveyStates(StatesGroup):
    # 1. Покупали ли предметы искусства
    q1_bought_art = State()
    q1_bought_art_other = State()

    # 2. Считаете ли, что разбираетесь в искусстве
    q2_expertise = State()

    # 3. Трудности при выборе искусства
    q3_difficulties = State()
    q3_difficulties_other = State()

    # 4. Что будем искать
    q4_what_to_search = State()
    q4_goal = State()
    q4_goal_other = State()
    
    # 5. Цвета для утра
    q5_colors = State()

    # 6. Любимые художники / фотографы / скульпторы (текст)
    q6_favorite_authors = State()

    # 7. Референсы (файлы)
    q7_references = State()

    # 8. Настроение, которое хотите создать (текст)
    q8_mood = State()

    # 9. Пожелания при подборе (текст)
    q9_wishes = State()

    # 10. Размер пространства (варианты)
    q10_size = State()
    q10_size_other = State()

    # 11. Желаемый формат
    q11_format = State()
    q11_format_other = State()

    # 12. Фото интерьера (файлы)
    q12_interior_photos = State()

    # 13. Бюджет
    q13_budget = State()

    # 14. Страна доставки
    q14_delivery_country = State()

    # 15. Хобби и увлечения
    q15_hobbies = State()
    q15_hobbies_other = State()

    # 16. Как предпочитаете получать предложения
    q16_contact_method = State()

    # 17. Контакт для связи
    q17_contact_details = State()

    # Завершение
    finished = State()
