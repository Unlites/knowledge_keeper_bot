from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.dto.record import CreateRecordDTO
from bot.handlers.utils.validation import validation_handler
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
        self._bot.send_message(message.chat.id, "Enter record topic")
        self._bot.register_next_step_handler(message, self._set_topic)

    @validation_handler
    def _set_topic(self, message: types.Message) -> None:
        self._dto.topic = message.text
        self._ask_title(message)
    
    def _ask_title(self, message: types.Message) -> None:
        self._bot.send_message(message.chat.id, "Enter record title")
        self._bot.register_next_step_handler(message, self._set_title)

    @validation_handler
    def _set_title(self, message: types.Message) -> None:
        self._dto.title = message.text
        self._ask_content(message)

    def _ask_content(self, message: types.Message) -> None:
        self._bot.send_message(message.chat.id, "Enter record content")
        self._bot.register_next_step_handler(message, self._set_content)

    @validation_handler
    def _set_content(self, message: types.Message) -> None:
        self._dto.content = message.text
        self._create_record(message)
        
    def _create_record(self, message: types.Message) -> None:
        self._usecase(message.chat.id, self._dto)