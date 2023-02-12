from telebot import types, TeleBot


class StartHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._handle(message)

    def _handle(self, message: types.Message):
        self._bot.send_message(
            message.chat.id, 
            "Welcome. Press /new_record to capture the recently acquired knowledge!"
        )
