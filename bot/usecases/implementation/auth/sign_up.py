from logging import Logger
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus
from bot.dto.user import RequestUserDTO
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.repository.token import TokenRepository
from bot.models.user import User
from bot.usecases.auth.sign_up import SignUpUsecase


class SignUpUsecaseImpl(SignUpUsecase):
    def __init__(
        self,
        logger: Logger,
        auth_api: KnowledgeKeeperAPIAuth,
        token_repo: TokenRepository,
    ) -> None:
        self._logger = logger
        self._auth_api = auth_api
        self._token_repo = token_repo

    def __call__(self, telegram_id, user_dto: RequestUserDTO) -> UsecaseResult:
        try:
            user = User(
                username=user_dto.username,
                password=user_dto.password,
            )
            self._auth_api.sign_up(user)

            tokens = self._auth_api.sign_in(user)
            self._token_repo.set_tokens(telegram_id, tokens)
            return UsecaseResult()
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id} - {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)

