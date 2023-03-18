import json
from telebot import types, TeleBot
from bot.handlers.record.base_get_records import BaseGetRecordsHandler


class GetAllRecordsHandler(BaseGetRecordsHandler):
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        super().__init__(message, bot)


class GetAllRecordsSwitchPageHandler(GetAllRecordsHandler):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._callback_data = json.loads(callback.data)
        super().__init__(callback.message, bot)

    def _handle(self, message: types.Message) -> None:
        self._get_records(
            message,
            current_page=self._callback_data["page"],
            is_callback=True,
        )
