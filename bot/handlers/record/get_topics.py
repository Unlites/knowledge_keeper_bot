from telebot import types, TeleBot
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, record_topics_markup
from bot.usecases.record.get_topics import GetTopicsUsecase


topics_cache = {}


class GetTopicsHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetTopicsUsecase)
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        result = self._usecase(message.chat.id)

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    message.chat.id,
                    "You haven't created records yet",
                )
                return

            self._bot.send_message(
                message.chat.id,
                "Choose neaded topic",
                reply_markup=record_topics_markup(result.data),
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
                f"Failed to get topics - {result.data}",
            )
