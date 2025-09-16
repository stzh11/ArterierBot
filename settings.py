
from pathlib import Path


BASE_DIR = Path(__file__).parent
images_path = Path(__file__).parent.parent / "static" / "images"

class Settings:
    BOT_TOKEN = "8333896356:AAERB58Gb6k6scltmwf25j053nShy49NySo"
    SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    ]
    Q4_IMG_PATH = BASE_DIR / "static" / "images" / "q4.png"
    Q4_ENG_IMG_PATH = BASE_DIR / "static" / "images" / "q4_eng.png"
    ADMIN_ACCOUNT_LIST = ["470629740"]
    DRIVE_FOLDER_Q7 = "1KanZ-MJB-7vQSIgEzFFg-ihuyvUKzI3y"
    DRIVE_FOLDER_Q12 = "1Adi8_J-RV3HRECOI-FfKrLEEPbB0_cTv"
    GOOGLE_AUTH_TOKEN_PATH = BASE_DIR / "bot/token.json"
    GOOGLE_CLIENT_SECRET_PATH = BASE_DIR / "client_secret.json"
    Q5_IMAGES = {
    "mono":     BASE_DIR  / "static" / "images" / "mono.jpg",
    "warm":     BASE_DIR  / "static" / "images" / "warm.jpg",
    "cold":     BASE_DIR  / "static" / "images" / "cold.jpg",
    "contrast": BASE_DIR  / "static" / "images" / "contrast.jpg",
    "bw":       BASE_DIR  / "static" / "images" / "bw.jpg",
    }
    q5_options = [
        ("mono", "Монохром"),
        ("warm", "Тёплые цвета"),
        ("cold", "Более холодная гамма"),
        ("contrast", "Контрасты и энергия"),
        ("bw", "Чёрно-белое"),
    ]
    MAX_FILES = 5

    q1_options = [
        ("yes", "Да"),
        ("no", "Нет"),
        ("other", "Другое")
    ]  
    q2_options = [
        ("def_yes", "Я - профессионал"),
        ("rather_yes", "Скорее хорошо"),
        ("hard_to_say", "Затрудняюсь ответить"),
        ("rather_no", "Скорее не разбираюсь"),
        ("def_no", "Ничего в нем не понимаю"),
    ]
    q3_options = [
        ("time", "Требует слишком много времени на выбор"),
        ("price", "Сложно оценить, насколько справедлива цена"),
        ("interior", "Нет уверенности, что впишется в интерьер"),
        ("choice", "Сложно сделать выбор"),
        ("expensive", "Искусство - это дорого"),
        ("other", "Другое")
    ]
    q4_options = [
        ("paintings", "Картины"),
        ("graphics", "Графику"),
        ("photos", "Фотографии"),
        ("posters", "Плакаты"),
        ("caricatures", "Карикатуры"),
        ("sculpture", "Скульптуры"),
    ]
    q4_goal_options = [
        ("living_room", "В гостинной"),
        ("bedroom", "В спальне"),
        ("hall", "В прихожей"),
        ("children_room", "В детской"),
        ("work_room", "В кабинете"),
        ("office", "В офисе"),
        ("single",  "Для всего дома / квартиры"),
        ("curated", "Для общественных / деловых помещений"),
    ]
    q10_options = [
        ("10x20", "10 x 20 см"),
        ("15x30", "15 x 30 см"),
        ("20x30", "20 x 30 см"),
        ("30x40", "30 x 40 см"),
        ("40x60", "40 x 60 см"),
        ("50x70", "50 x 70 см"),
        ("70x90", "70 x 90 см"),
        ("90x120", "90 x 120 см"),
        ("other", "Другое"),
    ]
    q11_options = [
        ("horizontal", "Горизонтальный"),
        ("vertical", "Вертикальный"),
        ("square", "Квадрат"),
        ("any", "Не важно"),
        ("other", "Другое"),
    ]
    q13_options = [
        ("<1000", "< 100,000 ₽"),
        ("1000-2499", "100,000-250,000 ₽"),
        ("2500-4999", "250,000-500,000 ₽"),
        ("5000-10000", "500,000-1,000,000 ₽"),
        (">10000", "> 1,000,000 ₽"),
    ]
    q15_options = [
        ("team_sport", "Командные виды спорта"),
        ("ind_sport", "Индивидуальный спорт"),
        ("extreme_sport", "Экстремальный спорт"),
        ("finance", "Финансы и инвестиции"),
        ("extreme_travel", "Экстремальные путешествия"),
        ("concerts", "Концерты"),
        ("theatre", "Театры и музеи"),
        ("travel", "Новые страны"),
        ("nature", "Отдых на природе"),
        ("music", "Музыка"),
        ("books", "Книги"),
        ("cinema", "Кино"),
        ("science", "Наука"),
        ("engineering", "Инженерия"),
        ("other", "Другое"),
    ]
    q16_options = [
        ("telegram", "Telegram"),
        ("whatsapp", "WhatsApp"),
        ("email", "E-mail"),
    ]

    LOCALES = {
    "ru": {
        # Кнопки
        "buttons.done": "Дальше",
        "buttons.back": "Назад",
        "buttons.skip": "Пропустить",
        "buttons.select": "Выбрать",

        # Тексты вопросов
        "q1.text":  "Покупали ли Вы когда-нибудь предметы искусства?",
        "q2.text":  "Насколько хорошо Вы разбираетесь в искусстве?",
        "q3.text":  "Что вызывает наибольшие сложности при выборе произведений искусства для Вашего дома?",
        "q4.text":  "Что будем искать?",
        "q4_goal.text": "Где планируется разместить художественное произведение?",
        "q5.text":  "Какие цвета Вы хотели бы видеть в своем пространстве каждый день?",
        "q6.text":  "Ваши любимые художники/фотографы/скульпторы? Напишите в одном сообщении.",
        "q7.text":  "Какими референсами Вам хочется поделиться? Пришлите до 5 фото, можно альбомом.",
        "q8.text":  "Какое настроение Вы хотите создать в этом пространстве?",
        "q9.text":  "Какие Ваши пожелания мы должны учесть при подборе произведений искусства? Что для Вас важно? "
        "Вам больше нравятся сюжетные понятные картины, пейзажи, портреты или абстракция, фактура, цвет?"
        "Расскажите о своем отношении к искусству, что-то важное о себе и об интерьере, чтобы мы лучше Вас поняли."
        "чувствовать при взгляде на Ваше новое произведение искусства",
        "q10.text": "Какой размер пространства хочется украсить?",
        "q11.text": "Выберите подходящий размер произведения искусства:",
        "q12.text": "Вы можете загрузить до 5 фотографий интерьера.",
        "q13.text": "Ваш ориентировочный бюджет?",
        "q14.text": "В какой город надо доставить Ваше произведение искусства?",
        "q15.text": "Ваши хобби и увлечения:",
        "q16.text": "Как предпочитаете получать предложения?",
        "q17.text": "Оставьте контакт (ник в Telegram / номер / email):",

        # Подписи опций (ключи из Settings)
        "q1_options": dict(q1_options),
        "q2_options": dict(q2_options),
        "q3_options": dict(q3_options),
        "q4_options": dict(q4_options),
        "q4_goal_options": dict(q4_goal_options),
        "q5_options": dict(q5_options),
        "q10_options": dict(q10_options),
        "q11_options": dict(q11_options),
        "q13_options": dict(q13_options),
        "q15_options": dict(q15_options),
        "q16_options": dict(q16_options),
    },

    "en": {
        "buttons.done": "Next",
        "buttons.back": "Back",
        "buttons.skip": "Skip",
        "buttons.select": "Select",

        "q1.text":  "Have you ever bought art?",
        "q2.text":  "How well do you know art?",
        "q3.text":  "What is most challenging when choosing art for your home?",
        "q4.text":  "What shall we look for?",
        "q4_goal.text": "Where is the artwork planned to be placed?",
        "q5.text":  "What colors would you like to see in your space every day?",
        "q6.text":  "Your favorite artists/photographers/sculptors? Write in one message.",
        "q7.text":  "What references would you like to share? Send photos (up to 5, may be an album).",
        "q8.text":  "What mood would you like to create in this space?",
        "q9.text": "What are your wishes that we should take into account when choosing live art? What is important to you?" 
        "Do you prefer plot and clear paintings, landscapes, portraits or abstraction, texture, color?" 
        "Tell us about your attitude to art, something important to you and about the interior, so that we can understand you better.",
        "q10.text": "What size of space would you like to decorate?",
        "q11.text": "Select the appropriate size of the artwork:",
        "q12.text": "You can upload up to 5 photos of the interior.",
        "q13.text": "What is your estimated budget??",
        "q14.text": "To which city should your piece of art be delivered?",
        "q15.text": "Your hobbies and interests:",
        "q16.text": "How do you prefer to receive proposals?",
        "q17.text": "Leave a contact (Telegram handle / phone / email):",

        "q1_options": {
            "yes": "Yes", "no": "No", "other": "Other"
        },
        "q2_options": {
            "def_yes": "I'm a professional",
            "rather_yes": "Rather good",
            "hard_to_say": "Hard to say",
            "rather_no": "I don't really understand it",
            "def_no": "I don't understand anything about it.",
        },
        "q3_options": {
            "time": "Takes too much time",
            "price": "Hard to understand if the price is fair",
            "interior": "Not sure it will fit the interior",
            "choice": "Difficult to choose",
            "expensive": "Art is expensive",
            "other": "Other",
        },
        "q4_options": {
            "paintings": "Paintings         ",
            "graphics": "Graphics",
            "photos": "Photos",
            "posters": "Posters",
            "caricatures": "Caricatures",
            "sculpture": "Sculptures",
        },
        "q4_goal_options": {
            "living_room": "In the living room",
            "bedroom": "In the bedroom",
            "hall": "In the hallway",
            "children_room": "In the child's room",
            "work_room": "In the home office",
            "office": "In the office",
            "single": "For the whole home / apartment",
            "curated": "For public / business spaces",
        },
        "q5_options": {
            "mono": "Monochrome",
            "warm": "Warm colors",
            "cold": "Colder palette",
            "contrast": "Contrasts & energy",
            "bw": "Black & white",
        },
        "q10_options": {
            "10x20": "10 x 20 cm",
            "15x30": "15 x 30 cm",
            "20x30": "20 x 30 cm",
            "30x40": "30 x 40 cm",
            "40x60": "40 x 60 cm",
            "50x70": "50 x 70 cm",
            "70x90": "70 x 90 cm",
            "90x120": "90 x 120 cm",
            "other": "Other",
        },
        "q11_options": {
            "horizontal": "Horizontal",
            "vertical": "Vertical",
            "square": "Square",
            "any": "Doesn't matter",
            "other": "Other",
        },
        "q13_options": {
            "<1000": "< 1,000 $/€",
            "1000-2499": "1,000–2,499 $/€",
            "2500-4999": "2,500–4,999 $/€",
            "5000-10000": "5,000–10,000 $/€",
            ">10000": ">10,000 $/€",
        },
        "q15_options": {
            "team_sport": "Team sports",
            "ind_sport": "Individual sports",
            "extreme_sport": "Extreme sports",
            "finance": "Finance & investing",
            "concerts": "Concerts",
            "theatre": "Theatres & museums",
            "travel": "New countries",
            "extreme_travel": "Extreme travelling",
            "nature": "Outdoor recreation",
            "music": "Music",
            "books": "Books",
            "cinema": "Cinema",
            "science": "Science",
            "engineering": "Engineering",
            "other": "Other",
        },
        "q16_options": {
            "telegram": "Telegram",
            "whatsapp": "WhatsApp",
            "email": "E-mail",
        },
    },
}


