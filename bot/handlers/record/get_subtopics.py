import json
from bot.usecases.record.get_subtopics import GetSubtopicsUsecase
from telebot import types, TeleBot
from bot.cache.cache import Cache
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, record_subtopics_markup


class GetSubtopicsHandler:
    def __init__(self, callback: types.CallbackQuery, bot: TeleBot) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetSubtopicsUsecase)
        self._callback_data = json.loads(callback.data)
        self._cache = di_container.resolve(Cache)
        self._handle(callback.message)

    def _handle(self, message: types.Message) -> None:
        user_cache = self._cache.get_user_cache(message.chat.id)
        topic = user_cache.found_topics[self._callback_data["topic_id"]]["value"]

        result = self._usecase(message.chat.id, topic)

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    message.chat.id,
                    "Can't find any record with subtopic \U0001F937\u200D\u2642\uFE0F",
                )
                return

            subtopics = []
            for i in range(len(result.data)):
                subtopics.append({"id": i, "value": result.data[i]})

            user_cache.found_subtopics = subtopics
            self._cache.set_user_cache(message.chat.id, user_cache)

            self._bot.send_message(
                message.chat.id,
                "Choose neaded subtopic",
                reply_markup=record_subtopics_markup(subtopics),
            )
        elif result.status == UsecaseStatus.UNAUTHORIZED:
            self._bot.send_message(
                message.chat.id,
                "You have to sign in! \u26D4\uFE0F",
                reply_markup=auth_markup(message.chat.id),
            )
        else:
            self._bot.send_message(
                message.chat.id,
                f"Failed to get subtopics - {result.data}  \U0001F6AB",
            )
