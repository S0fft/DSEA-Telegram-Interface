import telebot
from decouple import config

from parsing.main import schedule_parser

TOKEN = config('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Some message')


@bot.message_handler(commands=['schedule'])
def send_schedule(message):
    url = 'http://www.dgma.donetsk.ua/13-09-22-rozklad-dzvinkiv.html'
    schedule = schedule_parser(url)

    for line in schedule:
        bot.send_message(message.chat.id, line)


bot.polling()
