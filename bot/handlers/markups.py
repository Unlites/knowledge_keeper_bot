import json
from telebot import types
from bot.dto.record import GetRecordDTO
from bot.handlers.utils.pagination import Pagination
from config.config import Config


def auth_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    sign_in_page = types.WebAppInfo(Config.SIGN_IN_URL)
    sign_up_page = types.WebAppInfo(Config.SIGN_UP_URL)

    sign_in_button = types.KeyboardButton(text="Sign In", web_app=sign_in_page)
    sign_up_button = types.KeyboardButton(text="Sign Up", web_app=sign_up_page)

    markup.add(sign_in_button, sign_up_button)

    return markup


def _add_pagination_btns(
    markup: types.InlineKeyboardMarkup, pagination: Pagination
) -> types.InlineKeyboardMarkup:
    if pagination.next_page:
        next_btn = types.InlineKeyboardButton(
            "Next page", callback_data=pagination.next_page
        )
        markup.add(next_btn)

    if pagination.prev_page:
        prev_btn = types.InlineKeyboardButton(
            "Previous page", callback_data=pagination.prev_page
        )
        markup.add(prev_btn)

    return markup


def record_titles_markup(
    record_dtos: list[GetRecordDTO], pagination: Pagination
) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    for record_dto in record_dtos:
        btn = types.InlineKeyboardButton(
            record_dto.title,
            callback_data=json.dumps(
                {"operation": "get_record_by_id", "id": record_dto.id}
            ),
        )
        markup.add(btn)

    markup = _add_pagination_btns(markup, pagination)

    return markup
