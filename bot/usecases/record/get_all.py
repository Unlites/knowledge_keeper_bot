from abc import ABC, abstractmethod
from bot.dto.usecase_result import UsecaseResult


class GetAllRecordsUsecase(ABC):
    @abstractmethod
    def __call__(
        self,
        telegram_id,
        limit,
        offset,
        topic=None,
        subtopic=None,
        title=None,
    ) -> UsecaseResult:
        pass
