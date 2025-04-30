from io import BytesIO

import requests
import telebot
from decouple import config
from telebot import types
from telebot.types import InputFile

from parsing.main import call_schedule_parser, class_schedule_parser

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)

# -----------------------------------------------------------------------------------

schedule_cache = {}

COURSE_LABELS = [
    "1 курс", "2 курс", "3 курс", "4 курс",
    "Прискорений курс (2 семестр)",
    "Прискорений курс (4 семестр)",
    "Магістри (1 курс)"
]


# -----------------------------------------------------------------------------------

@bot.message_handler(commands=['call_schedule'])
def send_call_schedule(message):
    text, image_url, page_url = call_schedule_parser()
    text = "\n".join(text) + "\n\n" + f'Джерело: {page_url}'
    response = requests.get(image_url, stream=True)

    bot.send_photo(message.chat.id, response.raw, caption=text)


# -----------------------------------------------------------------------------------

@bot.message_handler(commands=['class_schedule'])
def send_class_schedule(message):
    text, image_urls, page_url = class_schedule_parser()
    text = f"{text}\n\nДжерело: {page_url}"

    for image_url in image_urls:
        response = requests.get(image_url)

        if response.status_code == 200:
            image_data = BytesIO(response.content)
            bot.send_document(message.chat.id, document=image_data, caption=text)
        else:
            bot.send_message(message.chat.id, f"Error loading image: {image_url}")

# -----------------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
def send_bot_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton('Moodle')
    button2 = types.KeyboardButton('Web-ресурси та соціальні мережі ДДМА')
    button3 = types.KeyboardButton('Розклад дзвінків')
    button4 = types.KeyboardButton('Розклад занять')
    button5 = types.KeyboardButton('Розклад сесії')
    button6 = types.KeyboardButton('Рейтинг студентів')
    button7 = types.KeyboardButton('Стипендіальні списки')
    button8 = types.KeyboardButton('Табель-календар')
    button9 = types.KeyboardButton('About')

    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)

    bot.send_message(
        message.chat.id,
        'Вітаю, я бот ДДМА! Я створений для того, щоб допомагати Вам!',
        reply_markup=markup
    )


# -----------------------------------------------------------------------------------

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type != 'private':
        pass

    chat_id = message.chat.id
    text = message.text

    if text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton('Moodle')
        button2 = types.KeyboardButton('Web-ресурси та соціальні мережі ДДМА')
        button3 = types.KeyboardButton('Розклад дзвінків')
        button4 = types.KeyboardButton('Розклад занять')
        button5 = types.KeyboardButton('Розклад сесії')
        button6 = types.KeyboardButton('Рейтинг студентів')
        button7 = types.KeyboardButton('Стипендіальні списки')
        button8 = types.KeyboardButton('Табель-календар')
        button9 = types.KeyboardButton('About')

        markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)

        bot.send_message(
            message.chat.id, 'Назад', reply_markup=markup)

# -----------------------------------------------------------------------------------

    if text == 'Web-ресурси та соціальні мережі ДДМА':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Офіційний Сайт')
        button2 = types.KeyboardButton('YouTube')
        button3 = types.KeyboardButton('Telegram')
        button4 = types.KeyboardButton('Telegram-чат')
        button5 = types.KeyboardButton('LinkedIn')
        button6 = types.KeyboardButton('Instagram')
        button7 = types.KeyboardButton('Facebook')
        button8 = types.KeyboardButton('Facebook: Медіа-Група ДДМА')
        button9 = types.KeyboardButton('Кафедра ІСПР')
        button10 = types.KeyboardButton('Назад')

        markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
        bot.send_message(chat_id, 'Виберіть одну з опцій:', reply_markup=markup)

# -----------------------------------------------------------------------------------

    if text == 'Розклад дзвінків':
        bot.send_message(message.chat.id, 'Отримую інформацію...')
        send_call_schedule(message)

# -----------------------------------------------------------------------------------

    if text == 'Розклад занять':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('1 курс')
        btn2 = types.KeyboardButton('2 курс')
        btn3 = types.KeyboardButton('3 курс')
        btn4 = types.KeyboardButton('4 курс')
        btn5 = types.KeyboardButton('Прискорений курс (2 семестр)')
        btn6 = types.KeyboardButton('Прискорений курс (4 семестр)')
        btn7 = types.KeyboardButton('Магістри (1 курс)')
        btn8 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

        bot.send_message(chat_id, 'Виберіть одну з опцій:', reply_markup=markup)

        title, image_urls, page_url = class_schedule_parser()
        schedule_cache[chat_id] = (title, image_urls, page_url)

# -----------------------------------------------------------------------------------

    if text in COURSE_LABELS:
        if chat_id not in schedule_cache:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Розклад занять'))

            bot.send_message(chat_id, 'Будь ласка, натисніть "Розклад занять". Йде обробка даних...',
                             reply_markup=markup)
            return

        bot.send_message(chat_id, 'Отримую інформацію...')

        title, image_urls, page_url = schedule_cache[chat_id]
        idx = COURSE_LABELS.index(text)

        try:
            url = image_urls[idx]
        except (IndexError, TypeError):
            bot.send_message(chat_id, "Не вдалося знайти розклад для цього курсу.")

        resp = requests.get(url)

        if resp.status_code == 200:
            bio = BytesIO(resp.content)
            filename = f"{text}.png"
            bio.name = filename
            caption = f"{title} — {text}\n\nДжерело: {page_url}"
            bot.send_document(chat_id, document=bio, caption=caption)
        else:
            bot.send_message(chat_id, f"Error loading: {url}")

    def go_to_website(msg, link):
        inline = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text=msg.text, url=link)
        inline.add(btn)

        bot.send_message(msg.chat.id, "Посилання на ресурс:", reply_markup=inline)

# -----------------------------------------------------------------------------------

    if text == "Moodle":
        go_to_website(message, "http://moodle-new.dgma.donetsk.ua/")

    if text == "Офіційний Сайт":
        go_to_website(message, "http://www.dgma.donetsk.ua/")

    if text == "YouTube":
        go_to_website(message, "https://www.youtube.com/user/mediagrupaAcademia")

    if text == "Telegram":
        go_to_website(message, "https://t.me/ddma_official")

    if text == "Telegram-чат":
        go_to_website(message, "https://bit.ly/36Wc2kB")

    if text == "LinkedIn":
        go_to_website(message, "https://www.linkedin.com/school/donbas-state-engineering-academy-dsea/")

    if text == "Instagram":
        go_to_website(message, "https://www.instagram.com/ddma_official/")

    if text == "Facebook":
        go_to_website(message, "https://www.facebook.com/ddma.kramatorsk/")

    if text == "Facebook: Медіа-Група ДДМА":
        go_to_website(message, "https://www.facebook.com/groups/mediagrupa/")

    if text == "Кафедра ІСПР":
        go_to_website(message, "http://www.dgma.donetsk.ua/~kiber/")

    # if text == 'Розклад сесії':
    #     pass

    # if text == 'Рейтинг студентів':
    #     pass

    # if text == 'Стипендіальні списки':
    #     pass

    # if text == 'Табель-календар':
    #     pass

    # if text == 'About':
    #     pass


# -----------------------------------------------------------------------------------

bot.polling()
