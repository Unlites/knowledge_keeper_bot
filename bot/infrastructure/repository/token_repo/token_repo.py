from abc import ABC, abstractmethod
from bot.models.tokens import Tokens


class TokenRepository(ABC):
    @abstractmethod
    def get_tokens_by_tg_id(self, telegram_id) -> Tokens | None:
        pass

    @abstractmethod
    def set_tokens(self, telegram_id, tokens: Tokens) -> None:
        pass
