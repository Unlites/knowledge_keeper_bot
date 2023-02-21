import json
from telebot import types, TeleBot
from bot.di_container.container import di_container
from bot.dto.user import UserSignUpDTO
from bot.handlers.utils.validation import validation_handler
from bot.usecases.auth.sign_up import SignUpUsecase


class SignUpHandler:
    def __init__(self, message: types.Message, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(SignUpUsecase)
        self._handle(message)
    
    @validation_handler
    def _handle(self, message: types.Message) -> None:
        data = json.loads(message.web_app_data.data)

        userDTO = UserSignUpDTO(
            username=data["username"],
            password=data["password"],
            confirm_password=data["confirm_password"]
        )

        result = self._usecase(message.chat.id, userDTO)
        markup = types.ReplyKeyboardRemove()
        
        if result.success:
            self._bot.send_message(
                message.chat.id, 
                "Sign up is successful! You can use this bot.", 
                reply_markup=markup
            )
        else:
            self._bot.send_message(message.chat.id, f"Sign up is failed: {result.data}")