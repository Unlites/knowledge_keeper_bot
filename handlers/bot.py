from telebot import types, TeleBot
from os import environ as env

bot = TeleBot(env['BOT_TOKEN'])

bot.set_my_commands([
    types.BotCommand("/new_record", "Create a new record")
])

@bot.message_handler(commands=['start'])
def command_handler(message):
    bot.send_message(
        message.chat.id, 
        "Welcome. Press /new_record to capture the recently acquired knowledge!"
    )