import requests
import telebot
from decouple import config

from parsing.main import call_schedule_parser

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Message!')


@bot.message_handler(commands=['schedule', 'расписание', 'розклад'])
def send_call_schedule(message):
    schedule_text, image_url, page_url = call_schedule_parser()

    text = "\n".join(schedule_text) + "\n"*2 + f'Джерело: {page_url}'
    response = requests.get(image_url, stream=True)

    bot.send_photo(message.chat.id, response.raw, caption=text)


bot.polling()
