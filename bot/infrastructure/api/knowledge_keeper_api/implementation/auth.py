import requests
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from config.config import Config
from bot.models.user import User
from bot.models.tokens import Tokens


class KnowledgeKeeperAPIAuthImpl(KnowledgeKeeperAPIAuth):
    def __init__(self) -> None:
        self._url = Config.API_URL + "/auth"

    def sign_in(self, user: User):
        pass

    def refresh(self, tokens: Tokens):
        pass