import json
from telebot import TeleBot, types
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, cancelation_markup
from bot.usecases.record.delete import DeleteRecordUsecase


class DeleteRecordHandler:
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(DeleteRecordUsecase)
        self._callback_data = json.loads(callback.data)
        self._handle(callback)

    def _handle(self, callback: types.CallbackQuery) -> None:
        self._ask_confirmation(callback.message)

    def _ask_confirmation(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            'Confirm deleting record by writing "YES"',
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._check_confirmation)

    def _check_confirmation(self, message) -> None:
        if message.text == "YES":
            self._delete_record(message)
        else:
            self._send_message(message.chat.id, "Deleting canceled")

    def _delete_record(self, message: types.Message) -> None:
        result = self._usecase(
            message.chat.id,
            self._callback_data["id"],
        )

        if result.status == UsecaseStatus.SUCCESS:
            self._bot.send_message(
                message.chat.id,
                "Record deleted successully! \u2705",
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
                f"Failed to delete record - {result.data} \U0001F6AB",
            )
