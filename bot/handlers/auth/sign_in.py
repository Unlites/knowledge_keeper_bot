from logging import Logger
from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.usecases.auth.sign_in import SignInUsecase


class SignInHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._logger = di_container.resolve(Logger)
        self._usecase = di_container.resolve(SignInUsecase)
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        result = self._usecase(None)
        if result.success:
            self._bot.send_message(message.chat.id, "Login is successful!")
        else:
            self._bot.send_message(message.chat.id, f"Login is failed: {result.data}")