from pydantic import ValidationError
from telebot import types
from bot.handlers.utils import message_converting


def validation(func):
    def decorator(self, message: types.Message, *args, **kwargs):
        try:
            func(self, message, *args, **kwargs)
        except ValidationError as e:
            self._bot.send_message(
                message.chat.id, 
                f"Input values is incorrect:\
                {message_converting.validation_errors(e.errors())}"
            )
    return decorator
