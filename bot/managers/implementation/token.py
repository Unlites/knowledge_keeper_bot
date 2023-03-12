from bot.infrastructure.api.errors import UnauthorizedError
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.repository.token_repo.token_repo import TokenRepository


class TokenManagerImpl:
    def __init__(
        self,
        auth_api: KnowledgeKeeperAPIAuth,
        token_repo: TokenRepository,
    ) -> None:
        self._auth_api = auth_api
        self._token_repo = token_repo
        self.with_tokens_refresh = False

    def manage_tokens(self, telegram_id) -> str:
        tokens = self._token_repo.get_tokens_by_tg_id(telegram_id)

        if not tokens:
            raise UnauthorizedError

        if self.with_tokens_refresh:
            tokens = self._auth_api.refresh(tokens.refresh_token)
            self._token_repo.set_tokens(telegram_id, tokens)

        return tokens.access_token
