import json
from telebot import TeleBot
from telebot.types import CallbackQuery
from bot.di_container.container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup
from bot.handlers.message_converting import displaying_record
from bot.usecases.record.get_by_id import GetRecordByIdUsecase


class GetRecordByIdHandler:
    def __init__(self, callback: CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetRecordByIdUsecase)
        self._handle(callback)

    def _handle(self, callback: CallbackQuery) -> None:
        result = self._usecase(
            callback.message.chat.id,
            record_id=json.loads(callback.data)["id"],
        )

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(callback.message.chat.id, "Record not found")
                return

            self._bot.send_message(
                callback.message.chat.id,
                displaying_record(result.data),
                parse_mode="markdown",
            )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                callback.message.chat.id,
                "You have to sign in!",
                reply_markup=auth_markup(),
            )
        else:
            self._bot.send_message(
                callback.message.chat.id, f"Failed to get record - {result.data}"
            )
