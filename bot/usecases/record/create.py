from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult
from bot.dto.record import CreateRecordDTO


class CreateRecordUsecase(ABC):
    @abstractmethod
    def __call__(self, telegram_id, record_dto: CreateRecordDTO) -> UsecaseResult:
        pass