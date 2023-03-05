import json
from telebot import types, TeleBot
from bot.handlers.record.create import CreateRecordHandler
from bot.handlers.start import StartHandler
from bot.handlers.auth.sign_in import SignInHandler
from bot.handlers.auth.sign_up import SignUpHandler
from bot.handlers.record.search_by_title import SearchByTitleHandler
from config.config import Config


def create_bot() -> TeleBot:
    bot = TeleBot(Config.BOT_TOKEN)

    bot.set_my_commands(
        [
            types.BotCommand("/create", "Create a new record"),
            types.BotCommand("/get_all", "Get all records"),
            types.BotCommand("/search", "Search records by title"),
        ]
    )

    return bot


def register_handlers(bot: TeleBot) -> None:
    command_handlers = {
        "start": StartHandler,
        "create": CreateRecordHandler,
        "search": SearchByTitleHandler,
    }

    web_app_handlers = {"sign_in": SignInHandler, "sign_up": SignUpHandler}

    for command, handler in command_handlers.items():
        bot.register_message_handler(handler, commands=[command], pass_bot=True)

    for operation, handler in web_app_handlers.items():
        bot.register_message_handler(
            handler,
            content_types=["web_app_data"],
            func=_web_app_operation_filter(operation),
            pass_bot=True,
        )


def run(bot: TeleBot) -> None:
    bot.infinity_polling()


def _web_app_operation_filter(operation):
    return (
        lambda message: json.loads(message.web_app_data.data)["operation"] == operation
    )
