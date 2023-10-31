from telebot import types, TeleBot
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.dto.user import RequestUserDTO
from bot.handlers.markups import cancelation_markup
from bot.handlers.middleware import validation
from bot.usecases.auth.sign_up import SignUpUsecase


class SignUpHandler:
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(SignUpUsecase)
        self._dto = RequestUserDTO()
        self._handle(callback.message)

    def _handle(self, message: types.Message) -> None:
        self._ask_username(message)

    def _ask_username(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter your username \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_username)

    @validation
    def _set_username(self, message: types.Message) -> None:
        self._dto.username = message.text
        self._ask_password(message)

    def _ask_password(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Enter your password \U0001F4DD",
            reply_markup=cancelation_markup(),
        )
        self._bot.register_next_step_handler(message, self._set_password)

    @validation
    def _set_password(self, message: types.Message) -> None:
        self._dto.password = message.text
        self._sign_up(message)

    def _sign_up(self, message: types.Message) -> None:
        result = self._usecase(message.chat.id, self._dto)
        if result.status == UsecaseStatus.SUCCESS:
            self._bot.send_message(
                message.chat.id,
                "Successfull sign up! \u2705",
            )
        else:
            self._bot.send_message(
                message.chat.id,
                f"Failed to sign up - {result.data} \U0001F6AB",
            )
