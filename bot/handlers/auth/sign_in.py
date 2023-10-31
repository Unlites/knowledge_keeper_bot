from telebot import types, TeleBot
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.dto.user import RequestUserDTO
from bot.handlers.markups import cancelation_markup
from bot.handlers.middleware import validation
from bot.usecases.auth.sign_in import SignInUsecase


class SignInHandler:
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(SignInUsecase)
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
        self._sign_in(message)

    def _sign_in(self, message: types.Message) -> None:
        result = self._usecase(message.chat.id, self._dto)
        if result.status == UsecaseStatus.SUCCESS:
            self._bot.send_message(
                message.chat.id,
                "Successfull sign in! \u2705",
            )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                message.chat.id,
                "Incorrect login or password \u26D4\uFE0F",
            )
        else:
            self._bot.send_message(
                message.chat.id,
                f"Failed to sign in - {result.data} \U0001F6AB",
            )
