from abc import ABC, abstractmethod
from bot.dto.user import UserSignInDTO
from bot.dto.usecase_result import UsecaseResult


class SignInUsecase(ABC):
    @abstractmethod
    def __call__(self, userDTO: UserSignInDTO) -> UsecaseResult:
        pass