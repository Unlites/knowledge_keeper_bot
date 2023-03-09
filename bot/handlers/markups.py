import json
from telebot import types
from bot.dto.record import GetRecordDTO
from bot.handlers.callback_data import CallbackOperation
from config.config import Config


def auth_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    sign_in_page = types.WebAppInfo(Config.SIGN_IN_URL)
    sign_up_page = types.WebAppInfo(Config.SIGN_UP_URL)

    sign_in_button = types.KeyboardButton(text="Sign In", web_app=sign_in_page)
    sign_up_button = types.KeyboardButton(text="Sign Up", web_app=sign_up_page)

    markup.add(sign_in_button, sign_up_button)

    return markup


def record_titles_markup(record_dtos: list[GetRecordDTO]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    for record_dto in record_dtos:
        btn = types.InlineKeyboardButton(
            record_dto.title,
            callback_data=json.dumps(
                {
                    "operation": CallbackOperation.GET_RECORD_BY_ID.value,
                    "id": record_dto.id,
                }
            ),
        )
        markup.add(btn)

    return markup
