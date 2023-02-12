from bot.dto.user import UserDTO
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.usecases.auth.sign_in import SignInUsecase
from bot.usecases.result import UsecaseResult


class SignInUsecaseImpl(SignInUsecase):
    def __init__(self, knowledge_keeper_api_auth: KnowledgeKeeperAPIAuth) -> None:
        self._api = knowledge_keeper_api_auth

    def __call__(self, userDTO: UserDTO) -> UsecaseResult:
        try:
            self._api.sign_in(userDTO)
            return UsecaseResult()
        except Exception as e:
            return UsecaseResult(e, success=False)