import json
import requests
from requests.exceptions import ConnectionError
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError, UnauthorizedError
from bot.infrastructure.api.errors import KnowledgeKeeperAPIConnectionError
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from http import HTTPStatus
from bot.infrastructure.api.utils.request import do_request
from config.config import Config
from bot.models.user import User
from bot.models.tokens import Tokens


class KnowledgeKeeperAPIAuthImpl(KnowledgeKeeperAPIAuth):
    def __init__(self) -> None:
        self._url = Config.API_URL + "/auth"

    def sign_in(self, user: User) -> Tokens:
        data = do_request(
            "POST",
            f"{self._url}/sign_in",
            body=user.json(),
        )

        return Tokens(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
        )

    def sign_up(self, user: User) -> None:
        do_request(
            "POST",
            f"{self._url}/sign_up",
            body=user.json(),
        )

    def refresh(self, refresh_token) -> Tokens:
        data = do_request(
            "POST",
            f"{self._url}/refresh",
            body=json.dumps({"refresh_token": refresh_token}),
        )

        return Tokens(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
        )
