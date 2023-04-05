from abc import ABC, abstractmethod
from bot.models.record import Record


class KnowledgeKeeperAPIRecord(ABC):
    @abstractmethod
    def create(self, access_token, record: Record) -> None:
        pass

    @abstractmethod
    def get_all(
        self,
        access_token,
        limit,
        offset,
        topic=None,
        subtopic=None,
        title=None,
    ) -> list[Record]:
        pass

    @abstractmethod
    def get_by_id(self, access_token, record_id) -> Record:
        pass

    @abstractmethod
    def get_topics(self, access_token) -> list[str]:
        pass

    @abstractmethod
    def get_subtopics(self, access_token, topic) -> list[str]:
        pass

    @abstractmethod
    def update(self, access_token, record_id, record: Record) -> None:
        pass

    @abstractmethod
    def delete(self, access_token, record_id) -> None:
        pass
