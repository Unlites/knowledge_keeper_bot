from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, record_titles_markup
from bot.handlers.utils.pagination import Pagination
from bot.usecases.record.search_by_title import SearchByTitleUsecase


class SearchByTitleHandler:
    def __init__(self, message: types.Message, bot: TeleBot):
        self._bot = bot
        self._usecase = di_container.resolve(SearchByTitleUsecase)
        self._handle(message)

    def _handle(self, message: types.Message):
        self._ask_title(message)

    def _ask_title(self, message: types.Message):
        message = self._bot.send_message(message.chat.id, "Enter searching title")
        self._bot.register_next_step_handler(message, self._search)

    def _search(self, message: types.Message):
        pagination = Pagination(current_page=1)
        result = self._usecase(
            message.chat.id,
            message.text,
            pagination.limit_for_check_next_page,
            pagination.offset,
        )

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    message.chat.id, "Not found records contain this title"
                )
                return

            if len(result.data) < pagination.limit:
                pagination.next_page = 0

            self._bot.send_message(
                message.chat.id,
                "Choose neaded title",
                reply_markup=record_titles_markup(result.data, pagination),
            )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                message.chat.id, "You have to sign in!", reply_markup=auth_markup()
            )
        else:
            self._bot.send_message(
                message.chat.id, f"Failed to search records - {result.data}"
            )
