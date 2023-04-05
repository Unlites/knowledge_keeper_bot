from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.infrastructure.api.utils.headers import bearer_authorization
from bot.infrastructure.api.utils.request import do_request
from bot.models.record import Record
from config.config import Config


class KnowledgeKeeperAPIRecordImpl(KnowledgeKeeperAPIRecord):
    def __init__(self) -> None:
        self._url = Config.API_URL + "/record"

    def create(self, access_token, record: Record) -> None:
        do_request(
            "POST",
            self._url,
            body=record.json(),
            headers=bearer_authorization(access_token),
        )

    def get_all(
        self,
        access_token,
        limit,
        offset,
        topic=None,
        subtopic=None,
        title=None,
    ) -> list[Record]:
        data = do_request(
            "GET",
            self._url,
            params={
                "topic": topic,
                "subtopic": subtopic,
                "title": title,
                "limit": limit,
                "offset": offset,
            },
            headers=bearer_authorization(access_token),
        )
        records = []
        for record in data:
            records.append(
                Record(
                    id=record["id"],
                    topic=record["topic"],
                    subtopic=record["subtopic"],
                    title=record["title"],
                    content=record["content"],
                )
            )

        return records

    def get_by_id(self, access_token, record_id) -> Record:
        data = do_request(
            "GET",
            f"{self._url}/{record_id}",
            headers=bearer_authorization(access_token),
        )

        return Record(
            id=data["id"],
            topic=data["topic"],
            subtopic=data["subtopic"],
            title=data["title"],
            content=data["content"],
        )

    def get_topics(self, access_token) -> list[str]:
        return do_request(
            "GET",
            f"{self._url}/topics",
            headers=bearer_authorization(access_token),
        )

    def get_subtopics(self, access_token, topic) -> list[str]:
        return do_request(
            "GET",
            f"{self._url}/subtopics",
            params={"topic": topic},
            headers=bearer_authorization(access_token),
        )

    def update(self, access_token, record_id, record: Record) -> None:
        do_request(
            "PUT",
            f"{self._url}/{record_id}",
            body=record.json(),
            headers=bearer_authorization(access_token),
        )

    def delete(self, access_token, record_id) -> None:
        do_request(
            "DELETE",
            f"{self._url}/{record_id}",
            headers=bearer_authorization(access_token),
        )
