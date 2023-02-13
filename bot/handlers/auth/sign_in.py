from logging import Logger
from config.config import Config
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
        markup = types.InlineKeyboardMarkup(row_width=1)
        sign_in_page = types.WebAppInfo(Config.SIGN_IN_URL)
        button = types.InlineKeyboardButton(text="Sign In", web_app=sign_in_page)
        markup.add(button)

        self._bot.send_message(message.chat.id, "Please sign in for use this bot", reply_markup=markup)

        result = self._usecase(None)
        if result.success:
            self._bot.send_message(message.chat.id, "Sign in is successful!")
        else:
            self._bot.send_message(message.chat.id, f"Sign in is failed: {result.data}")