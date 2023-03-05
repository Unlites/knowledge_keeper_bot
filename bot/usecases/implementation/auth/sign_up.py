from logging import Logger
from bot.dto.user import UserSignUpDTO
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.repository.token_repo.token_repo import TokenRepository
from bot.models.user import User
from bot.usecases.auth.sign_up import SignUpUsecase
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus


class SignUpUsecaseImpl(SignUpUsecase):
    def __init__(
        self,
        logger: Logger,
        knowledge_keeper_api_auth: KnowledgeKeeperAPIAuth,
        token_repo: TokenRepository,
    ) -> None:
        self._logger = logger
        self._api = knowledge_keeper_api_auth
        self._token_repo = token_repo

    def __call__(self, telegram_id, userDTO: UserSignUpDTO) -> UsecaseResult:
        try:
            user = User(username=userDTO.username, password=userDTO.password)
            self._api.sign_up(user)
            tokens = self._api.sign_in(user)
            self._token_repo.set_tokens(telegram_id, tokens)
            return UsecaseResult()
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id}: {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)
