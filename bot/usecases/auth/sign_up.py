from abc import ABC, abstractmethod
from bot.dto.user import UserSignUpDTO
from bot.dto.usecase_result import UsecaseResult


class SignUpUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, userDTO: UserSignUpDTO) -> UsecaseResult:
        pass
