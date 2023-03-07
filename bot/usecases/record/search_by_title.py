from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult


class SearchRecordsByTitleUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, title, limit, offset) -> UsecaseResult:
        pass
