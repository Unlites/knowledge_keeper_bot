from abc import ABC, abstractmethod
from bot.models.user import User
from bot.models.tokens import Tokens


class KnowledgeKeeperAPIAuth(ABC):
    @abstractmethod
    def sign_in(self, user: User):
        pass
    
    @abstractmethod
    def sign_up(self, user: User):
        pass