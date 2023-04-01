from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult
from bot.dto.record import RequestRecordDTO


class CreateRecordUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, record_dto: RequestRecordDTO) -> UsecaseResult:
        pass
