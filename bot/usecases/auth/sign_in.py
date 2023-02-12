from abc import ABC, abstractmethod
from bot.dto.user import UserDTO
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth


class SignInUseCase(ABC):
    @abstractmethod
    def __call__(self, userDTO: UserDTO) -> None:
        pass