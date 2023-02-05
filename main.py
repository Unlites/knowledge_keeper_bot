from dotenv import load_dotenv
from telebot import TeleBot
from os import environ as env
from logging import StreamHandler, Formatter
import sys
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_handler = StreamHandler(stream=sys.stdout)
log_handler.setFormatter(Formatter(fmt='%(asctime)s: %(levelname)s %(message)s'))
log.addHandler(log_handler)

load_dotenv()

bot = TeleBot(env['BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def ping(message):
    bot.send_message(message.chat.id, "pong")

log.info("Starting bot...")
bot.infinity_polling()