import json
from telebot import types
from bot.dto.record import GetRecordDTO
from bot.handlers.callback_data import CallbackOperation
from config.config import Config


def auth_markup(telegram_id) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    sign_in_button = types.InlineKeyboardButton(
        text="Sign In",
        url=f"{Config.SIGN_IN_URL}?tg_id={telegram_id}",
    )

    sign_up_button = types.InlineKeyboardButton(
        text="Sign Up",
        url=f"{Config.SIGN_UP_URL}?tg_id={telegram_id}",
    )

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


def record_topics_markup(topics: list[str]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for topic in topics:
        btn = types.InlineKeyboardButton(
            topic,
            callback_data=json.dumps(
                {
                    "operation": CallbackOperation.GET_RECORDS_BY_TOPIC.value,
                    "topic": topic,
                }
            ),
        )
        markup.add(btn)

    return markup


def cancelation_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        "Cancel \u2716",
        callback_data=json.dumps(
            {
                "operation": CallbackOperation.CANCEL.value,
            }
        ),
    )
    markup.add(btn)

    return markup
