import requests
import telebot
from decouple import config
from telebot import types

from parsing.main import call_schedule_parser, class_schedule_parser

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # ddma = types.InlineKeyboardButton('Web-ресурси', url='http://www.dgma.donetsk.ua/')
    ddma = types.InlineKeyboardButton('Visit Website', url='http://www.dgma.donetsk.ua/')
    ddma2 = types.InlineKeyboardButton('Visit Website', url='http://www.dgma.donetsk.ua/')

    markup.add(ddma, ddma2)

    bot.send_message(message.chat.id, 'Click the button to visit the website:', reply_markup=markup)


# ---------------------------------------------------


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
