from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult


class DeleteRecordUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, record_id) -> UsecaseResult:
        pass
