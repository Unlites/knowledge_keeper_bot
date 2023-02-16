from bot.dto.user import UserSignUpDTO
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.models.user import User
from bot.usecases.auth.sign_up import SignUpUsecase
from bot.dto.usecase_result import UsecaseResult


class SignUpUsecaseImpl(SignUpUsecase):
    def __init__(self, knowledge_keeper_api_auth: KnowledgeKeeperAPIAuth) -> None:
        self._api = knowledge_keeper_api_auth

    def __call__(self, userDTO: UserSignUpDTO) -> UsecaseResult:
        try:
            user = User(
                username=userDTO.username,
                password=userDTO.password
            )
            self._api.sign_up(user)
            return UsecaseResult()
        except Exception as e:
            return UsecaseResult(e, success=False)