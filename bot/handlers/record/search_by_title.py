import json
from logging import Logger
from telebot import types, TeleBot
from bot.di_container import di_container
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.record.get_all import BaseGetRecordsHandler
from bot.usecases.record.get_all import GetAllRecordsUsecase


class SearchRecordsByTitleHandler(BaseGetRecordsHandler):
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetAllRecordsUsecase)
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        self._ask_title(message)

    def _ask_title(self, message: types.Message) -> None:
        message = self._bot.send_message(
            message.chat.id, "Enter searching title \U0001F4DD"
        )
        self._bot.register_next_step_handler(message, self._search)

    def _search(self, message: types.Message) -> None:
        title = message.text
        self._get_records(
            message,
            pagination_operation=CallbackOperation.SEARCH_RECORDS_BY_TITLE_SWITCH_PAGE,
            title=title,
            displayed_message_text="Results by searching title: " + title,
        )


class SearchRecordsByTitleSwitchPageHandler(SearchRecordsByTitleHandler):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._callback_data = json.loads(callback.data)
        super().__init__(callback.message, bot)

    def _handle(self, message) -> None:
        title = message.text.split(": ")[1]
        self._get_records(
            message,
            title=title,
            current_page=self._callback_data["page"],
            is_callback=True,
            pagination_operation=CallbackOperation.SEARCH_RECORDS_BY_TITLE_SWITCH_PAGE,
            displayed_message_text="Results by searching title: " + title,
        )
