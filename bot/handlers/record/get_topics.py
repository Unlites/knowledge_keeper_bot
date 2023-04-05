from bot.handlers.callback_data import CallbackOperation
from telebot import types, TeleBot
from bot.cache.cache import Cache
from bot.di_container import di_container
from bot.dto.usecase_result import UsecaseStatus
from bot.handlers.markups import auth_markup, record_topics_markup
from bot.usecases.record.get_topics import GetTopicsUsecase


class GetTopicsHandler:
    def __init__(
        self,
        message: types.Message,
        bot: TeleBot,
        next_operation: CallbackOperation = CallbackOperation.GET_RECORDS_BY_TOPIC,
    ) -> None:
        self._bot = bot
        self._usecase = di_container.resolve(GetTopicsUsecase)
        self._cache = di_container.resolve(Cache)
        self._next_operation = next_operation
        self._handle(message)

    def _handle(self, message: types.Message) -> None:
        result = self._usecase(message.chat.id)

        if result.status == UsecaseStatus.SUCCESS:
            if not result.data:
                self._bot.send_message(
                    message.chat.id,
                    "You haven't created records yet",
                )
                return

            topics = []
            for i in range(len(result.data)):
                topics.append({"id": i, "value": result.data[i]})

            user_cache = self._cache.get_user_cache(message.chat.id)
            user_cache.found_topics = topics
            self._cache.set_user_cache(message.chat.id, user_cache)

            self._bot.send_message(
                message.chat.id,
                "Choose neaded topic",
                reply_markup=record_topics_markup(topics, self._next_operation),
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
                f"Failed to get topics - {result.data} \U0001F6AB",
            )
