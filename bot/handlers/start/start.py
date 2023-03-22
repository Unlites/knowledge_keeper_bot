from telebot import types, TeleBot
from bot.handlers.markups import auth_markup


class StartHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        self._bot.send_message(
            message.chat.id,
            "Welcome! You have to sign in. Press button 'Sign In' for this or 'Sign Up'"
            + " if you need to create a new account",
            reply_markup=auth_markup(message.chat.id),
        )
