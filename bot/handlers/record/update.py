import json
from telebot import TeleBot, types
from bot.di_container import di_container
from bot.dto.record import RequestRecordDTO
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, cancelation_markup
from bot.handlers.middleware import validation
from bot.usecases.record.update import UpdateRecordUsecase


class UpdateRecordHandler:
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(UpdateRecordUsecase)
        self._dto = RequestRecordDTO()
        self._callback_data = json.loads(callback.data)
        self._handle(callback.message)

    def _handle(self, message: types.Message) -> None:
        self._ask_topic(message)

    def _ask_topic(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record topic or '-' to skip \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_topic)

    @validation
    def _set_topic(self, message: types.Message) -> None:
        if message.text != "-":
            self._dto.topic = message.text

        self._ask_subtopic(message)

    def _ask_subtopic(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record subtopic or '-' to skip \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_subtopic)

    @validation
    def _set_subtopic(self, message: types.Message) -> None:
        if message.text != "-":
            self._dto.subtopic = message.text
        self._ask_title(message)

    def _ask_title(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record title or '-' to skip \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_title)

    @validation
    def _set_title(self, message: types.Message) -> None:
        if message.text != "-":
            self._dto.title = message.text
        self._ask_content(message)

    def _ask_content(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record content or '-' to skip \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_content)

    @validation
    def _set_content(self, message: types.Message) -> None:
        if message.text != "-":
            self._dto.content = message.text
        self._update_record(message)

    def _update_record(self, message: types.Message) -> None:
        result = self._usecase(message.chat.id, self._callback_data["id"], self._dto)
        if result.status == UsecaseStatus.SUCCESS:
            self._bot.send_message(
                message.chat.id,
                "Record updated successfully! \u2705",
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
                f"Failed to update record - {result.data} \U0001F6AB",
            )
