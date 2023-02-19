import requests
from requests.exceptions import ConnectionError
from bot.infrastructure.api.errors import KnowledgeKeeperAPIConnectionError, KnowledgeKeeperAPIError
from http import HTTPStatus
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from config.config import Config
from bot.models.user import User
from bot.models.tokens import Tokens


class KnowledgeKeeperAPIAuthImpl(KnowledgeKeeperAPIAuth):
    def __init__(self) -> None:
        self._url = Config.API_URL + "/auth"

    def sign_in(self, user: User) -> Tokens:
        try:
            response = requests.post(
                f"{self._url}/sign_in",
                data=user.json()
            )
            
            data = response.json()['data']
            if response.status_code != HTTPStatus.OK:
                raise KnowledgeKeeperAPIError(data)

            return Tokens(
                access_token=data['access_token'],
                refresh_token=data['refresh_token']
            )
        except ConnectionError as e:
            raise KnowledgeKeeperAPIConnectionError(e)
    
    def sign_up(self, user: User) -> None:
        try:
            response = requests.post(
                f"{self._url}/sign_up",
                data=user.json()
            )
            
            data = response.json()['data']
            if response.status_code != HTTPStatus.OK:
                raise KnowledgeKeeperAPIError(data)
        except ConnectionError as e:
            raise KnowledgeKeeperAPIConnectionError(e)

    def refresh(self, tokens: Tokens):
        pass