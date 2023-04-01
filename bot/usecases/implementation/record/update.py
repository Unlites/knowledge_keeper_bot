from logging import Logger
from bot.dto.record import RequestRecordDTO
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.errors import UnauthorizedError
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.managers.token import TokenManager
from bot.models.record import Record
from bot.usecases.record.update import UpdateRecordUsecase


class UpdateRecordUsecaseImpl(UpdateRecordUsecase):
    def __init__(
        self,
        logger: Logger,
        record_api: KnowledgeKeeperAPIRecord,
        token_manager: TokenManager,
    ) -> None:
        self._logger = logger
        self._record_api = record_api
        self._token_manager = token_manager

    def __call__(
        self, telegram_id, record_id, record_dto: RequestRecordDTO
    ) -> UsecaseResult:
        try:
            access_token = self._token_manager.manage_tokens(telegram_id)

            record = Record(
                topic=record_dto.topic,
                title=record_dto.title,
                content=record_dto.content,
            )
            self._record_api.update(access_token, record_id, record)

            return UsecaseResult()
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id} - {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)
        except UnauthorizedError:
            if self._token_manager.with_tokens_refresh:
                return UsecaseResult(status=UsecaseStatus.UNAUTHORIZED)

            self._token_manager.with_tokens_refresh = True
            return self.__call__(telegram_id, record_id)
