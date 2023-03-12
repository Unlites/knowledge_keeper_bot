from abc import ABC, abstractmethod


class TokenManager(ABC):
    @abstractmethod
    def manage_tokens(self, telegram_id) -> str:
        pass
