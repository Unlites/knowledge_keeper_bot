import json
from bot.handlers import message_converting
from pydantic import ValidationError
from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.dto.user import UserSignUpDTO
from bot.usecases.auth.sign_in import SignInUsecase


class SignUpHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(SignInUsecase)
        self._handle(message)
    
    def _handle(self, message: types.Message) -> None:
        data = json.loads(message.web_app_data.data)
        try:
            userDTO = UserSignUpDTO(
                username=data["username"],
                password=data["password"],
                confirm_password=data["confirm_password"]
            )
        except ValidationError as e:
            self._bot.send_message(
                message.chat.id, 
                f"Input values is incorrect:{message_converting.validation_errors(e.errors())}"
            )
            return

        result = self._usecase(userDTO)
        markup = types.ReplyKeyboardRemove()
        
        if result.success:
            self._bot.send_message(
                message.chat.id, 
                "Sign up is successful!", 
                reply_markup=markup
            )
        else:
            self._bot.send_message(message.chat.id, f"Sign up is failed: {result.data}")