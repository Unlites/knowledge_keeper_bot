from telebot import types, TeleBot
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.callback_data import CallbackOperation
from bot.handlers.markups import auth_markup, record_titles_markup
from bot.handlers.pagination import Pagination
from bot.usecases.record.get_all import GetAllRecordsUsecase


class BaseGetRecordsHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetAllRecordsUsecase)
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        self._get_records(message)

    def _get_records(
        self,
        message: types.Message,
        current_page=1,
        is_callback=False,
        topic=None,
        title=None,
        pagination_operation=CallbackOperation.GET_ALL_RECORDS_SWITCH_PAGE,
        displayed_message_text="Choose neaded title",
    ) -> None:
        pagination = Pagination(current_page)

        result = self._usecase(
            message.chat.id,
            pagination.limit_for_check_next_page,
            pagination.offset,
            topic=topic,
            title=title,
        )

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    message.chat.id,
                    "Records not found \U0001F937\u200D\u2642\uFE0F",
                )
                return

            if len(result.data) < pagination.limit_for_check_next_page:
                pagination.next_page = 0

            titles_markup = record_titles_markup(result.data[: pagination.limit])
            paginated_titles_markup = pagination.paginate(
                titles_markup,
                operation=pagination_operation,
            )

            if is_callback:
                self._bot.edit_message_text(
                    displayed_message_text,
                    message.chat.id,
                    message.id,
                    reply_markup=paginated_titles_markup,
                )
            else:
                self._bot.send_message(
                    message.chat.id,
                    displayed_message_text,
                    reply_markup=paginated_titles_markup,
                )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                message.chat.id,
                "You have to sign in! \u26D4\uFE0F",
                reply_markup=auth_markup(message.chat.id),
            )
        else:
            self._bot.send_message(
                message.chat.id,
                f"Failed to get records - {result.data} \U0001F6AB",
            )
