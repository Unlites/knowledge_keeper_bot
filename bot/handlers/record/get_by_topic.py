import json
from logging import Logger
from telebot import types, TeleBot
from bot.di_container import di_container
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.record.get_all import BaseGetRecordsHandler
from bot.usecases.record.get_all import GetAllRecordsUsecase


class GetRecordsByTopic(BaseGetRecordsHandler):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetAllRecordsUsecase)
        self._callback_data = json.loads(callback.data)
        self._handle(callback.message)

    def _handle(self, message: types.Message) -> None:
        self._get_records(
            message,
            topic=self._callback_data["topic"],
            pagination_operation=CallbackOperation.GET_RECORDS_BY_TOPIC_SWITCH_PAGE,
        )


class GetRecordsByTopicSwitchPageHandler(GetRecordsByTopic):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._callback_data = json.loads(callback.data)
        super().__init__(callback, bot)

    def _handle(self, message) -> None:
        di_container.resolve(Logger).info(self._callback_data["topic"])
        self._get_records(
            message,
            topic=self._callback_data["topic"],
            current_page=self._callback_data["page"],
            is_callback=True,
            pagination_operation=CallbackOperation.GET_RECORDS_BY_TOPIC_SWITCH_PAGE,
        )
