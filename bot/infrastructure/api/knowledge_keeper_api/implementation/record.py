import requests
from requests.exceptions import ConnectionError
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError, KnowledgeKeeperAPIUnauthorized
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
                headers=bearer_authorization(access_token)
            )
            
            data = response.json()['data']
            
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                raise KnowledgeKeeperAPIUnauthorized
            elif response.status_code != HTTPStatus.OK:
                raise KnowledgeKeeperAPIError(data)

        except ConnectionError as e:
            raise KnowledgeKeeperAPIConnectionError(e)
    