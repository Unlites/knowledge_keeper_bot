from abc import ABC, abstractmethod
from bot.models.user import User
from bot.models.record import Record


class KnowledgeKeeperAPIRecord(ABC):
    @abstractmethod
    def create_record(self, access_token, record: Record):
        pass
    