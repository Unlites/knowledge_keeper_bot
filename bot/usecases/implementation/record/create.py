from bot.dto.usecase_result import UsecaseResult
from bot.dto.record import CreateRecordDTO


class CreateRecordUsecaseImpl:
    def __call__(self, telegram_id, record_dto: CreateRecordDTO) -> UsecaseResult:
        pass