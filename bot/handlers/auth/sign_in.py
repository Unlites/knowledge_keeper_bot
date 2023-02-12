from logging import Logger
from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.usecases.auth.sign_in import SignInUseCase


class SignInHandler:
    def __init__(self, message: types.Message, bot: TeleBot):
        self._bot = bot
        self._logger = di_container.resolve(Logger)
        self._usecase = di_container.resolve(SignInUseCase)
        self._handle(message)

    def _handle(self, message: types.Message):
        result = self._usecase(None)
        self._bot.send_message(message.chat.id, result)