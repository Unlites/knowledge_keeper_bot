from abc import ABC, abstractmethod
from bot.models.record import Record


class KnowledgeKeeperAPIRecord(ABC):
    @abstractmethod
    def create_record(self, access_token, record: Record) -> None:
        pass

    @abstractmethod
    def search_by_title(self, access_token, title, limit, offset) -> list[Record]:
        pass

    @abstractmethod
    def get_by_id(self, access_token, record_id) -> Record:
        pass
