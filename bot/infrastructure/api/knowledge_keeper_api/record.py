from abc import ABC, abstractmethod
from bot.models.record import Record


class KnowledgeKeeperAPIRecord(ABC):
    @abstractmethod
    def create_record(self, access_token, record: Record) -> None:
        pass

    @abstractmethod
    def get_all_records(
        self,
        access_token,
        limit,
        offset,
        topic=None,
        title=None,
    ) -> list[Record]:
        pass

    @abstractmethod
    def get_by_id(self, access_token, record_id) -> Record:
        pass
