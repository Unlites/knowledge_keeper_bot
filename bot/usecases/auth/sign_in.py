from abc import ABC, abstractmethod
from bot.dto.user import UserDTO
from bot.usecases.result import UsecaseResult


class SignInUsecase(ABC):
    @abstractmethod
    def __call__(self, userDTO: UserDTO) -> UsecaseResult:
        pass