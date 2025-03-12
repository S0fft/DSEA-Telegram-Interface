import requests
import telebot
from decouple import config
from telebot import types

from parsing.main import call_schedule_parser, class_schedule_parser

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_bot_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton('Moodle')
    button2 = types.KeyboardButton('Web-ресурси та соціальні мережі ДДМА')
    button3 = types.KeyboardButton('Розклад дзвінків')
    button4 = types.KeyboardButton('Розклад пар')
    button5 = types.KeyboardButton('Розклад сесії')
    button6 = types.KeyboardButton('Рейтинг студентів')
    button7 = types.KeyboardButton('Стипендіальні списки')
    button8 = types.KeyboardButton('Табель-календар')
    button9 = types.KeyboardButton('About')

    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)

    bot.send_message(message.chat.id, 'Вітаю, я бот ДДМА! Я створений для того, щоб допомагати Вам!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            button1 = types.KeyboardButton('Moodle')
            button2 = types.KeyboardButton('Web-ресурси та соціальні мережі ДДМА')
            button3 = types.KeyboardButton('Розклад дзвінків')
            button4 = types.KeyboardButton('Розклад пар')
            button5 = types.KeyboardButton('Розклад сесії')
            button6 = types.KeyboardButton('Рейтинг студентів')
            button7 = types.KeyboardButton('Стипендіальні списки')
            button8 = types.KeyboardButton('Табель-календар')
            button9 = types.KeyboardButton('About')

            markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)

            bot.send_message(
                message.chat.id, 'Назад', reply_markup=markup)

        if message.text == 'Web-ресурси та соціальні мережі ДДМА':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            button1 = types.KeyboardButton('Офіційний Сайт')
            button2 = types.KeyboardButton('YouTube')
            button3 = types.KeyboardButton('Telegram')
            button4 = types.KeyboardButton('Telegram-Чат')
            button5 = types.KeyboardButton('LinkedIn')
            button6 = types.KeyboardButton('Facebook')
            button7 = types.KeyboardButton('Facebook: Медіа-Група ДДМА')
            button8 = types.KeyboardButton('Facebook: Деканат ФАМIT')
            button9 = types.KeyboardButton('Кафедра ІСПР')
            button10 = types.KeyboardButton('Назад')

            markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)

            bot.send_message(message.chat.id, 'Виберіть одну з опцій:', reply_markup=markup)

        if message.text == 'Розклад дзвінків':
            send_call_schedule(message)

        def go_to_website(message, link):
            inline_markup = types.InlineKeyboardMarkup()

            button_site = types.InlineKeyboardButton(text=message.text, url=link)
            inline_markup.add(button_site)

            bot.send_message(message.chat.id, "Посилання:", reply_markup=inline_markup)

        if message.text == "Офіційний Сайт":
            go_to_website(message, "http://www.dgma.donetsk.ua/")

        if message.text == "YouTube":
            go_to_website(message, "https://www.youtube.com/user/mediagrupaAcademia")


@bot.message_handler(commands=['call_schedule'])
def send_call_schedule(message):
    text, image_url, page_url = call_schedule_parser()

    text = "\n".join(text) + "\n"*2 + f'Джерело: {page_url}'
    response = requests.get(image_url, stream=True)

    bot.send_photo(message.chat.id, response.raw, caption=text)


@bot.message_handler(commands=['class_schedule'])
def send_class_schedule(message):
    text, image_urls, page_url = class_schedule_parser()

    text = text + "\n\n" + f'Джерело: {page_url}'

    image_urls_list = image_urls.splitlines()

    for image_url in image_urls_list:
        response = requests.get(image_url, stream=True)

        if response.status_code == 200:
            bot.send_photo(message.chat.id, response.raw, caption=text)
        else:
            bot.send_message(message.chat.id, "Error")


bot.polling()
