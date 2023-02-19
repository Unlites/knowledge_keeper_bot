from abc import ABC, abstractmethod
from bot.models.tokens import Tokens


class TokenRepository(ABC):
    @abstractmethod
    def get_access_token_by_tg_id(self, telegram_id) -> str:
        pass

    @abstractmethod
    def get_refresh_token_by_tg_id(self, telegram_id) -> str:
        pass

    @abstractmethod
    def set_tokens(self, tokens: Tokens) -> None:
        pass