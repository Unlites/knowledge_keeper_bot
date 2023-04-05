from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult


class GetSubtopicsUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, topic) -> UsecaseResult:
        pass
