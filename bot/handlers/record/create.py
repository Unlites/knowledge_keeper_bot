from telebot import types, TeleBot
from bot.di_container import di_container
from bot.dto.record import CreateRecordDTO
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, cancelation_markup
from bot.handlers.middleware import validation
from bot.usecases.record.create import CreateRecordUsecase


class CreateRecordHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(CreateRecordUsecase)
        self._dto = CreateRecordDTO()
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        self._ask_topic(message)

    def _ask_topic(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record topic \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_topic)

    @validation
    def _set_topic(self, message: types.Message) -> None:
        self._dto.topic = message.text
        self._ask_title(message)

    def _ask_title(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record title \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_title)

    @validation
    def _set_title(self, message: types.Message) -> None:
        self._dto.title = message.text
        self._ask_content(message)

    def _ask_content(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter record content \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_content)

    @validation
    def _set_content(self, message: types.Message) -> None:
        self._dto.content = message.text
        self._create_record(message)

    def _create_record(self, message: types.Message) -> None:
        result = self._usecase(message.chat.id, self._dto)
        if result.status == UsecaseStatus.SUCCESS:
            self._bot.send_message(
                message.chat.id,
                "Record created successfully! \u2705",
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
                f"Failed to create record - {result.data} \U0001F6AB",
            )
