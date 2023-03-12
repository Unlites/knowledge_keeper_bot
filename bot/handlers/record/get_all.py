import json
from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.markups import auth_markup, record_titles_markup
from bot.handlers.pagination import Pagination
from bot.usecases.record.search_by_title import GetAllRecordsUsecase


class GetAllRecordsHandler:
    def __init__(self, message: types.Message, bot: TeleBot):
        self._bot = bot
        self._usecase = di_container.resolve(GetAllRecordsUsecase)
        self._handle(message)

    def _handle(
        self,
        message: types.Message,
        current_page=1,
        is_callback=False,
    ):
        pagination = Pagination(current_page)
        result = self._usecase(
            message.chat.id,
            pagination.limit_for_check_next_page,
            pagination.offset,
        )

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    message.chat.id,
                    "You haven't created records yet",
                )
                return

            if len(result.data) < pagination.limit:
                pagination.next_page = 0

            titles_markup = record_titles_markup(result.data)
            paginated_titles_markup = pagination.paginate(
                titles_markup,
                operation=CallbackOperation.GET_ALL_RECORDS_SWITCH_PAGE,
            )

            if is_callback:
                self._bot.edit_message_text(
                    "Choose neaded title",
                    message.chat.id,
                    message.id,
                    reply_markup=paginated_titles_markup,
                )
            else:
                self._bot.send_message(
                    message.chat.id,
                    "Choose neaded title",
                    reply_markup=paginated_titles_markup,
                )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                message.chat.id,
                "You have to sign in!",
                reply_markup=auth_markup(),
            )
        else:
            self._bot.send_message(
                message.chat.id,
                f"Failed to get all records - {result.data}",
            )


class GetAllRecordsSwitchPageHandler(GetAllRecordsHandler):
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot):
        self._bot = bot
        self._usecase = di_container.resolve(GetAllRecordsUsecase)
        self._handle(
            callback.message,
            current_page=json.loads(callback.data)["page"],
            is_callback=True,
        )
