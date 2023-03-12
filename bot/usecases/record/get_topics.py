from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult


class GetTopicsUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id) -> UsecaseResult:
        pass
