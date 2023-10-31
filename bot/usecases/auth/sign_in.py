from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult
from bot.dto.user import RequestUserDTO


class SignInUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, user_dto: RequestUserDTO) -> UsecaseResult:
        pass
