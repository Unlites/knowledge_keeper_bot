from telebot import types, TeleBot
from config.config import Config


class StartHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        sign_in_page = types.WebAppInfo(Config.SIGN_IN_URL)
        sign_up_page = types.WebAppInfo(Config.SIGN_UP_URL)

        sign_in_button = types.KeyboardButton(text="Sign In", web_app=sign_in_page)
        sign_up_button = types.KeyboardButton(text="Sign Up", web_app=sign_up_page)

        markup.add(sign_in_button, sign_up_button)

        self._bot.send_message(message.chat.id, 
            "Welcome! You have to sign in. Press button 'Sign In' for this or 'Sign Up'" +\
            " if you need to create a new account",
            reply_markup=markup
        )
