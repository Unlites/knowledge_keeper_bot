from telebot import TeleBot
from os import environ as env


bot = TeleBot(env['BOT_TOKEN'])
