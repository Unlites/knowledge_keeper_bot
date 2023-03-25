from abc import ABC, abstractmethod
from bot.models.tokens import Tokens


class KnowledgeKeeperAPIAuth(ABC):
    @abstractmethod
    def refresh(self, refresh_token) -> Tokens:
        pass
