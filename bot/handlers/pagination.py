import json
from bot.handlers.callback_data import CallbackOperation
from config.config import Config
from telebot import types


class Pagination:
    def __init__(self, current_page) -> None:
        self.current_page = current_page
        self.next_page = current_page + 1
        self.prev_page = current_page - 1
        self.limit = Config.DISPLAY_LIMIT
        self.offset = self.limit * self.prev_page
        self.limit_for_check_next_page = self.limit + 1

    def paginate(
        self,
        markup: types.InlineKeyboardMarkup,
        operation: CallbackOperation,
        input_value=None,
    ) -> types.InlineKeyboardMarkup:
        if self.next_page:
            next_btn = types.InlineKeyboardButton(
                "Next page",
                callback_data=json.dumps(
                    {
                        "operation": operation.value,
                        "input_value": input_value,
                        "page": self.next_page,
                    }
                ),
            )
            markup.add(next_btn)

        if self.prev_page:
            prev_btn = types.InlineKeyboardButton(
                "Previous page",
                callback_data=json.dumps(
                    {
                        "operation": operation.value,
                        "input_value": input_value,
                        "page": self.prev_page,
                    }
                ),
            )
            markup.add(prev_btn)

        return markup
