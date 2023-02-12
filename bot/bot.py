from telebot import types, TeleBot
from bot.handlers.start import StartHandler
from bot.handlers.auth.sign_in import SignInHandler
from config.config import Config


def create_bot() -> TeleBot:
    bot = TeleBot(Config.BOT_TOKEN)

    bot.set_my_commands([
        types.BotCommand("/new_record", "Create a new record"),
        types.BotCommand("/get_all_records", "Get all records"),
        types.BotCommand("/get_record", "Get record"),
        types.BotCommand("/delete_record", "Delete a record"),
        types.BotCommand("/update_record", "Update a record"),
    ])

    return bot


def register_handlers(bot: TeleBot) -> None:
    command_handlers = {
        "start": StartHandler,
        "sign_in": SignInHandler,
    }
    
    for command, handler in command_handlers.items():
        bot.register_message_handler(handler, commands=[command], pass_bot=True)


def run(bot: TeleBot) -> None:
    bot.infinity_polling()