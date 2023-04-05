import json
from telebot import types, TeleBot
from bot.cache.cache import Cache
from bot.di_container import di_container
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.record.get_all import BaseGetRecordsHandler
from bot.usecases.record.get_all import GetAllRecordsUsecase


class GetRecordsByTopicHandler(BaseGetRecordsHandler):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetAllRecordsUsecase)
        self._cache = di_container.resolve(Cache)
        self._callback_data = json.loads(callback.data)
        self._handle(callback.message)

    def _handle(self, message: types.Message) -> None:
        self._get_records(
            message,
            topic=self._get_cached_topic(message.chat.id),
            pagination_operation=CallbackOperation.GET_RECORDS_BY_TOPIC_SWITCH_PAGE,
        )

    def _get_cached_topic(self, telegram_id) -> str:
        user_cache = self._cache.get_user_cache(telegram_id)
        return user_cache.found_topics[self._callback_data["topic_id"]]["value"]


class GetRecordsByTopicSwitchPageHandler(GetRecordsByTopicHandler):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._callback_data = json.loads(callback.data)
        super().__init__(callback, bot)

    def _handle(self, message) -> None:
        self._get_records(
            message,
            topic=self._get_cached_topic(message.chat.id),
            current_page=self._callback_data["page"],
            is_callback=True,
            pagination_operation=CallbackOperation.GET_RECORDS_BY_TOPIC_SWITCH_PAGE,
        )
