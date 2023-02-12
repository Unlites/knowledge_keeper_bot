from bot.dto.user import UserDTO
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.usecases.auth.sign_in import SignInUseCase


class SignInUseCaseImpl(SignInUseCase):
    def __init__(self, knowledge_keeper_api_auth: KnowledgeKeeperAPIAuth) -> None:
        self._api = knowledge_keeper_api_auth

    def __call__(self, userDTO: UserDTO) -> None:
        try:
            return self._api.sign_in(userDTO)
        except:
            return None