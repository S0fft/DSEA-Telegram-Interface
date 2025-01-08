import requests
import telebot
from decouple import config

from parsing.main import call_schedule_parser, class_schedule_parser

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Message!')


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

    response = requests.get(image_urls_list, stream=True)
    bot.send_photo(message.chat.id, response.content, caption=text)


bot.polling()
