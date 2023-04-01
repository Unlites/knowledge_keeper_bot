from logging import Logger
from bot.dto.record import ResponseRecordDTO
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.errors import UnauthorizedError
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.managers.token import TokenManager
from bot.usecases.record.get_by_id import GetRecordByIdUsecase


class GetRecordByIdUsecaseImpl(GetRecordByIdUsecase):
    def __init__(
        self,
        logger: Logger,
        record_api: KnowledgeKeeperAPIRecord,
        token_manager: TokenManager,
    ) -> None:
        self._logger = logger
        self._record_api = record_api
        self._token_manager = token_manager

    def __call__(self, telegram_id, record_id) -> UsecaseResult:
        try:
            access_token = self._token_manager.manage_tokens(telegram_id)

            record = self._record_api.get_by_id(access_token, record_id)

            record_dto = ResponseRecordDTO(
                id=record.id,
                topic=record.topic,
                title=record.title,
                content=record.content,
            )
            return UsecaseResult(record_dto)
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id} - {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)
        except UnauthorizedError:
            if self._token_manager.with_tokens_refresh:
                return UsecaseResult(status=UsecaseStatus.UNAUTHORIZED)

            self._token_manager.with_tokens_refresh = True
            return self.__call__(telegram_id, record_id)
