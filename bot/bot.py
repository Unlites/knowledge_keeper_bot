import json
from bot.handlers.auth.sign_in import SignInHandler
from bot.handlers.auth.sign_up import SignUpHandler
from bot.handlers.record.get_by_subtopic import (
    GetRecordsBySubtopicHandler,
    GetRecordsBySubtopicSwitchPageHandler,
)
from bot.handlers.record.get_subtopics import GetSubtopicsHandler
from bot.handlers.record.get_topics_for_subtopics import GetTopicsForSubtopicsHandler
from telebot import types, TeleBot
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.record.create import CreateRecordHandler
from bot.handlers.record.delete import DeleteRecordHandler
from bot.handlers.record.get_all import GetAllRecordsHandler
from bot.handlers.record.get_all import GetAllRecordsSwitchPageHandler
from bot.handlers.record.get_by_id import GetRecordByIdHandler
from bot.handlers.record.get_by_topic import (
    GetRecordsByTopicHandler,
    GetRecordsByTopicSwitchPageHandler,
)
from bot.handlers.record.get_topics import GetTopicsHandler
from bot.handlers.record.update import UpdateRecordHandler
from bot.handlers.start.start import StartHandler
from bot.handlers.record.search_by_title import SearchRecordsByTitleHandler
from bot.handlers.record.search_by_title import SearchRecordsByTitleSwitchPageHandler
from config.config import Config


def create_bot() -> TeleBot:
    bot = TeleBot(Config.BOT_TOKEN)

    bot.set_my_commands(
        [
            types.BotCommand(
                "/create",
                "Create a new record",
            ),
            types.BotCommand(
                "/get_by_subtopics",
                "Get all records by topic and subtopic",
            ),
            types.BotCommand(
                "/get_by_topic_only",
                "Get all records by chosen topic only",
            ),
            types.BotCommand(
                "/get_all_last",
                "Get all last records",
            ),
            types.BotCommand(
                "/search",
                "Search records by title",
            ),
        ]
    )

    return bot


def register_handlers(bot: TeleBot) -> None:
    command_handlers = {
        "start": StartHandler,
        "create": CreateRecordHandler,
        "search": SearchRecordsByTitleHandler,
        "get_all_last": GetAllRecordsHandler,
        "get_by_subtopics": GetTopicsForSubtopicsHandler,
        "get_by_topic_only": GetTopicsHandler,
    }

    callback_handlers = {
        CallbackOperation.GET_RECORD_BY_ID.value: GetRecordByIdHandler,
        CallbackOperation.GET_ALL_RECORDS_SWITCH_PAGE.value: GetAllRecordsSwitchPageHandler,
        CallbackOperation.SEARCH_RECORDS_BY_TITLE_SWITCH_PAGE.value: SearchRecordsByTitleSwitchPageHandler,
        CallbackOperation.GET_RECORDS_BY_TOPIC.value: GetRecordsByTopicHandler,
        CallbackOperation.GET_RECORDS_BY_TOPIC_SWITCH_PAGE.value: GetRecordsByTopicSwitchPageHandler,
        CallbackOperation.GET_SUBTOPICS.value: GetSubtopicsHandler,
        CallbackOperation.GET_RECORDS_BY_SUBTOPIC.value: GetRecordsBySubtopicHandler,
        CallbackOperation.GET_RECORDS_BY_SUBTOPIC_SWITCH_PAGE.value: GetRecordsBySubtopicSwitchPageHandler,
        CallbackOperation.UPDATE_RECORD.value: UpdateRecordHandler,
        CallbackOperation.DELETE_RECORD.value: DeleteRecordHandler,
        CallbackOperation.CANCEL.value: _remove_step_handler,
        CallbackOperation.SIGN_IN.value: SignInHandler,
        CallbackOperation.SIGN_UP.value: SignUpHandler,
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
