import json
from telebot import types, TeleBot
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.record.create import CreateRecordHandler
from bot.handlers.record.get_all import GetAllRecordsHandler
from bot.handlers.record.get_all import GetAllRecordsSwitchPageHandler
from bot.handlers.record.get_by_id import GetRecordByIdHandler
from bot.handlers.record.get_by_topic import GetRecordsByTopicSwitchPageHandler
from bot.handlers.record.get_by_topic import GetRecordsByTopic
from bot.handlers.record.get_topics import GetTopicsHandler
from bot.handlers.start.start import StartHandler
from bot.handlers.record.search_by_title import SearchRecordsByTitleHandler
from bot.handlers.record.search_by_title import SearchRecordsByTitleSwitchPageHandler
from config.config import Config


def create_bot() -> TeleBot:
    bot = TeleBot(Config.BOT_TOKEN)

    bot.set_my_commands(
        [
            types.BotCommand("/create", "Create a new record"),
            types.BotCommand("/get_all", "Get all records"),
            types.BotCommand("/get_topics", "Get all record topics"),
            types.BotCommand("/search", "Search records by title"),
        ]
    )

    return bot


def register_handlers(bot: TeleBot) -> None:
    command_handlers = {
        "start": StartHandler,
        "create": CreateRecordHandler,
        "search": SearchRecordsByTitleHandler,
        "get_all": GetAllRecordsHandler,
        "get_topics": GetTopicsHandler,
    }

    callback_handlers = {
        CallbackOperation.GET_RECORD_BY_ID.value: GetRecordByIdHandler,
        CallbackOperation.GET_ALL_RECORDS_SWITCH_PAGE.value: GetAllRecordsSwitchPageHandler,
        CallbackOperation.SEARCH_RECORDS_BY_TITLE_SWITCH_PAGE.value: SearchRecordsByTitleSwitchPageHandler,
        CallbackOperation.GET_RECORDS_BY_TOPIC.value: GetRecordsByTopic,
        CallbackOperation.GET_RECORDS_BY_TOPIC_SWITCH_PAGE.value: GetRecordsByTopicSwitchPageHandler,
        CallbackOperation.CANCEL.value: _remove_step_handler,
    }

    for command, handler in command_handlers.items():
        bot.register_message_handler(
            handler,
            commands=[command],
            pass_bot=True,
        )

    for operation, handler in callback_handlers.items():
        bot.register_callback_query_handler(
            handler,
            func=_callback_operation_filter(operation),
            pass_bot=True,
        )


def run(bot: TeleBot) -> None:
    bot.infinity_polling()


def _callback_operation_filter(operation):
    return lambda callback: json.loads(callback.data)["operation"] == operation


def _remove_step_handler(callback: types.CallbackQuery, bot: TeleBot):
    bot.send_message(callback.message.chat.id, "Canceled!")
    bot.clear_step_handler(callback.message)
