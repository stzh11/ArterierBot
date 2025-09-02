
from pathlib import Path
from utils.sheets import init_sheets

SHEET = init_sheets("Arterier Survey Results")

BASE_DIR = Path(__file__).parent.parent
images_path = Path(__file__).parent.parent / "static" / "images"

class Settings:
    BOT_TOKEN = "8333896356:AAERB58Gb6k6scltmwf25j053nShy49NySo"
    SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    ]
    DRIVE_FOLDER_Q7 = "1Adi8_J-RV3HRECOI-FfKrLEEPbB0_cTv"
    DRIVE_FOLDER_Q12 = "1KanZ-MJB-7vQSIgEzFFg-ihuyvUKzI3y"
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
        ("def_yes", "Точно да"),
        ("rather_yes", "Скорее да"),
        ("rather_no", "Скорее нет"),
        ("def_no", "Точно нет"),
        ("hard_to_say", "Затрудняюсь ответить"),
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
        ("single",  "Одно акцентное произведение искусства"),
        ("curated", "Кураторский подбор для всего интерьера"),
        ("other",   "Ваш вариант?"),
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
        ("<1000", "< 1,000 $/€"),
        ("1000-2499", "1,000-2,499 $/€"),
        ("2500-4999", "2,500-4,999 $/€"),
        ("5000-10000", "5,000-10,000 $/€"),
        (">10000", ">10,000 $/€"),
    ]
    q15_options = [
        ("team_sport", "Командные виды спорта"),
        ("ind_sport", "Индивидуальный спорт"),
        ("extreme_sport", "Экстремальный спорт"),
        ("finance", "Финансы и инвестиции"),
        ("concerts", "Посещение концертов"),
        ("theatre", "Посещение театров и музеев"),
        ("travel", "Путешествия по новым странам"),
        ("extreme_travel", "Экстремальные путешествия"),
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
        "buttons.done": "Готово",
        "buttons.back": "Назад",
        "buttons.skip": "Пропустить",
        "buttons.select": "Выбрать",

        # Тексты вопросов
        "q1.text":  "Покупали ли Вы когда-нибудь предметы искусства в галереях или у художников?",
        "q2.text":  "Считаете ли Вы, что разбираетесь в искусстве?",
        "q3.text":  "Что вызывает наибольшие сложности при выборе произведений искусства для Вашего дома?",
        "q4.text":  "Что будем искать?",
        "q4_goal.text": "Вы ищите:",
        "q5.text":  "Какие цвета Вы бы хотели видеть утром, просыпаясь? Выберите понравившиеся картины по цвету.",
        "q6.text":  "Ваши любимые художники/фотографы/скульпторы? Напишите в одном сообщении.",
        "q7.text":  "Есть ли у Вас референсы? Пришлите до 5 файлов (фото/PDF).",
        "q8.text":  "Какое настроение Вы хотите создать в этом пространстве?",
        "q9.text":  "Пожелания при подборе — что важно учесть?",
        "q10.text": "Какой размер пространства хочется украсить?",
        "q11.text": "Желаемый формат:",
        "q12.text": "Загрузите фото интерьера (до 5 фото, можно альбомом).",
        "q13.text": "Какой ориентировочный бюджет?",
        "q14.text": "Страна доставки:",
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
        "buttons.done": "Done",
        "buttons.back": "Back",
        "buttons.skip": "Skip",
        "buttons.select": "Select",

        "q1.text":  "Have you ever bought art in galleries or from artists?",
        "q2.text":  "Do you consider yourself knowledgeable about art?",
        "q3.text":  "What is most challenging when choosing art for your home?",
        "q4.text":  "What shall we look for?",
        "q4_goal.text": "You find:",
        "q5.text":  "Which colors would you like to see in the morning? Pick by color.",
        "q6.text":  "Your favorite artists/photographers/sculptors? Write in one message.",
        "q7.text":  "Do you have references? Send up to 5 files (images/PDF).",
        "q8.text":  "What mood would you like to create in this space?",
        "q9.text":  "Any wishes we should consider?",
        "q10.text": "What size of space would you like to decorate?",
        "q11.text": "Preferred format:",
        "q12.text": "Upload interior photos (up to 5, may be an album).",
        "q13.text": "Approximate budget?",
        "q14.text": "Delivery country:",
        "q15.text": "Your hobbies and interests:",
        "q16.text": "How do you prefer to receive proposals?",
        "q17.text": "Leave a contact (Telegram handle / phone / email):",

        "q1_options": {
            "yes": "Yes", "no": "No", "other": "Other"
        },
        "q2_options": {
            "def_yes": "Definitely yes",
            "rather_yes": "Rather yes",
            "rather_no": "Rather no",
            "def_no": "Definitely no",
            "hard_to_say": "Hard to say",
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
            "paintings": "Paintings",
            "graphics": "Graphics",
            "photos": "Photos",
            "posters": "Posters",
            "caricatures": "Caricatures",
            "sculpture": "Interior sculpture",
        },
        "q4_goal_options": {
            "single":  "Оne accent piece of art",
            "curated": "Сurated selection for the entire interior",
            "other":   "Other",
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
            "concerts": "Going to concerts",
            "theatre": "Theatres & museums",
            "travel": "Travelling to new countries",
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


