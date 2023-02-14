import json
from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.usecases.auth.sign_in import SignInUsecase


class SignInHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(SignInUsecase)
        self._handle(message)
    
    def _handle(self, message: types.Message) -> None:
        # data = json.loads(message.web_app_data.data)

        # if data["operation"] != "sign_in":
        #     return

        self._bot.send_message(message.chat.id, str(123))
        result = self._usecase(None)
        markup = types.ReplyKeyboardRemove()
        if result.success:
            self._bot.send_message(message.chat.id, "Sign in is successful!", reply_markup=markup)
        else:
            self._bot.send_message(message.chat.id, f"Sign in is failed: {result.data}")