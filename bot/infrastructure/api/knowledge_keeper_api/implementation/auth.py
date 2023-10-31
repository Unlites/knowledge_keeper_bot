import json
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.api.utils.request import do_request
from bot.models.user import User
from config.config import Config
from bot.models.tokens import Tokens


class KnowledgeKeeperAPIAuthImpl(KnowledgeKeeperAPIAuth):
    def __init__(self) -> None:
        self._url = Config.API_URL + "/auth"

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
    
    def sign_in(self, user: User) -> Tokens:
        data = do_request(
            "POST",
            f"{self._url}/sign_in",
            body=json.dumps({
                "username": user.username,
                "password": user.password,
            }),
        )

        return Tokens(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
        )
    
    def sign_up(self, user: User) -> None:
        do_request(
            "POST",
            f"{self._url}/sign_up",
            body=json.dumps({
                "username": user.username,
                "password": user.password,
            }),
        )
