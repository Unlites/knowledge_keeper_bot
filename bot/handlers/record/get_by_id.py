import json
from telebot import TeleBot, types
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, record_actions_markup
from bot.handlers.message_converting import displaying_record
from bot.usecases.record.get_by_id import GetRecordByIdUsecase


class GetRecordByIdHandler:
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetRecordByIdUsecase)
        self._handle(callback)

    def _handle(self, callback: types.CallbackQuery) -> None:
        record_id = json.loads(callback.data)["id"]

        result = self._usecase(
            callback.message.chat.id,
            record_id,
        )

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    callback.message.chat.id,
                    "Record not found \U0001F937\u200D\u2642\uFE0F",
                )
                return

            self._bot.send_message(
                callback.message.chat.id,
                displaying_record(result.data),
                parse_mode="html",
                reply_markup=record_actions_markup(record_id),
            )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                callback.message.chat.id,
                "You have to sign in! \u26D4\uFE0F",
                reply_markup=auth_markup(callback.message.chat.id),
            )
        else:
            self._bot.send_message(
                callback.message.chat.id,
                f"Failed to get record - {result.data} \U0001F6AB",
            )
