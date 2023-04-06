import json
from bot.handlers.callback_data import CallbackOperation
from config.config import Config
from telebot import types


class Pagination:
    def __init__(
        self,
        current_page,
        from_topic_id=None,
        from_subtopic_id=None,
    ) -> None:
        self.current_page = current_page
        self._from_topic_id = from_topic_id
        self._from_subtopic_id = from_subtopic_id
        self.next_page = current_page + 1
        self.prev_page = current_page - 1
        self.limit = Config.DISPLAY_LIMIT
        self.offset = self.limit * self.prev_page
        self.limit_for_check_next_page = self.limit + 1

    def paginate(
        self,
        markup: types.InlineKeyboardMarkup,
        operation: CallbackOperation,
    ) -> types.InlineKeyboardMarkup:
        callback_data = {
            "operation": operation.value,
        }

        if self._from_topic_id is not None:
            callback_data["topic_id"] = self._from_topic_id

        if self._from_subtopic_id is not None:
            callback_data["subtopic_id"] = self._from_subtopic_id

        if self.next_page:
            callback_data["page"] = self.next_page
            next_btn = types.InlineKeyboardButton(
                "Next page \u27A1",
                callback_data=json.dumps(callback_data),
            )
            markup.add(next_btn)

        if self.prev_page:
            callback_data["page"] = self.prev_page
            prev_btn = types.InlineKeyboardButton(
                "\u2B05 Previous page",
                callback_data=json.dumps(callback_data),
            )
            markup.add(prev_btn)

        return markup
