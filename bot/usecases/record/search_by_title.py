from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult


class SearchByTitleUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, title, limit, offset) -> UsecaseResult:
        pass
