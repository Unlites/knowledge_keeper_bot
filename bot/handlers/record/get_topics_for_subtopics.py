from bot.handlers.callback_data import CallbackOperation
from bot.handlers.record.get_topics import GetTopicsHandler
from telebot import TeleBot, types


class GetTopicsForSubtopicsHandler(GetTopicsHandler):
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._next_operation = CallbackOperation.GET_SUBTOPICS
        super().__init__(message, bot)
