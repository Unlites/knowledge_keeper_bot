from abc import ABC, abstractmethod
from bot.dto.record import RequestRecordDTO
from bot.dto.usecase_result import UsecaseResult


class UpdateRecordUsecase(ABC):
    @abstractmethod
    def __call__(
        self,
        telegram_id,
        record_id,
        record_dto: RequestRecordDTO,
    ) -> UsecaseResult:
        pass
