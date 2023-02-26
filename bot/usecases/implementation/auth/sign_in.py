from logging import Logger
from bot.dto.user import UserSignInDTO
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.repository.token_repo.token_repo import TokenRepository
from bot.models.user import User
from bot.usecases.auth.sign_in import SignInUsecase
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus


class SignInUsecaseImpl(SignInUsecase):
    def __init__(
        self, 
        logger: Logger, 
        knowledge_keeper_api_auth: KnowledgeKeeperAPIAuth,
        token_repo: TokenRepository
    ) -> None:
        self._logger = logger
        self._api = knowledge_keeper_api_auth
        self._token_repo = token_repo

    def __call__(self, telegram_id, userDTO: UserSignInDTO) -> UsecaseResult:
        try:
            user = User(
                username=userDTO.username,
                password=userDTO.password
            )
            tokens = self._api.sign_in(user)
            self._token_repo.set_tokens(telegram_id, tokens)
            return UsecaseResult()
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id}: {e.detail}")
            return UsecaseResult(e, UsecaseStatus.FAILURE)