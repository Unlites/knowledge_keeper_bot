import json
from telebot import types, TeleBot
from bot.handlers.record.create import CreateRecordHandler
from bot.handlers.start import StartHandler
from bot.handlers.auth.sign_in import SignInHandler
from bot.handlers.auth.sign_up import SignUpHandler
from config.config import Config


def create_bot() -> TeleBot:
    bot = TeleBot(Config.BOT_TOKEN)

    bot.set_my_commands([
        types.BotCommand("/create_record", "Create a new record"),
        types.BotCommand("/get_all_records", "Get all records"),
        types.BotCommand("/get_record", "Get record"),
        types.BotCommand("/delete_record", "Delete a record"),
        types.BotCommand("/update_record", "Update a record"),
    ])

    return bot


def register_handlers(bot: TeleBot) -> None:
    command_handlers = {
        "start": StartHandler,
        "create_record": CreateRecordHandler
    }

    web_app_handlers = {
        "sign_in": SignInHandler,
        "sign_up": SignUpHandler
    }
    
    for command, handler in command_handlers.items():
        bot.register_message_handler(handler, commands=[command], pass_bot=True)

    for operation, handler in web_app_handlers.items():
        bot.register_message_handler(
            handler, 
            content_types=["web_app_data"],
            func=_web_app_operation_filter(operation),
            pass_bot=True
        )


def run(bot: TeleBot) -> None:
    bot.infinity_polling()


def _web_app_operation_filter(operation):
    return lambda message: json.loads(message.web_app_data.data)["operation"] == operation