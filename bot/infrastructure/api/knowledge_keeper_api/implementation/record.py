import requests
from requests.exceptions import ConnectionError
from bot.infrastructure.api.errors import (
    KnowledgeKeeperAPIError,
    KnowledgeKeeperAPIUnauthorizedError,
)
from bot.infrastructure.api.errors import KnowledgeKeeperAPIConnectionError
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from http import HTTPStatus
from bot.infrastructure.api.utils.headers import bearer_authorization
from bot.models.record import Record
from config.config import Config


class KnowledgeKeeperAPIRecordImpl(KnowledgeKeeperAPIRecord):
    def __init__(self) -> None:
        self._url = Config.API_URL + "/record"

    def create_record(self, access_token, record: Record) -> None:
        try:
            response = requests.post(
                self._url,
                data=record.json(),
                headers=bearer_authorization(access_token),
            )

            data = response.json()["data"]

            if response.status_code == HTTPStatus.UNAUTHORIZED:
                raise KnowledgeKeeperAPIUnauthorizedError
            elif response.status_code != HTTPStatus.OK:
                raise KnowledgeKeeperAPIError(data)

        except ConnectionError as e:
            raise KnowledgeKeeperAPIConnectionError(e)

    def get_all_records(
        self,
        access_token,
        limit,
        offset,
        topic=None,
        title=None,
    ) -> list[Record]:
        try:
            response = requests.get(
                self._url,
                params={
                    "topic": topic,
                    "title": title,
                    "limit": limit,
                    "offset": offset,
                },
                headers=bearer_authorization(access_token),
            )

            data = response.json()["data"]
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                raise KnowledgeKeeperAPIUnauthorizedError
            elif response.status_code != HTTPStatus.OK:
                raise KnowledgeKeeperAPIError(data)

            records = []
            for record in data:
                records.append(
                    Record(
                        id=record["id"],
                        topic=record["topic"],
                        title=record["title"],
                        content=record["content"],
                    )
                )

            return records
        except ConnectionError as e:
            raise KnowledgeKeeperAPIConnectionError(e)

    def get_by_id(self, access_token, record_id) -> Record:
        try:
            response = requests.get(
                f"{self._url}/{record_id}",
                headers=bearer_authorization(access_token),
            )

            data = response.json()["data"]
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                raise KnowledgeKeeperAPIUnauthorizedError
            elif response.status_code != HTTPStatus.OK:
                raise KnowledgeKeeperAPIError(data)

            return Record(
                id=data["id"],
                topic=data["topic"],
                title=data["title"],
                content=data["content"],
            )

        except ConnectionError as e:
            raise KnowledgeKeeperAPIConnectionError(e)
