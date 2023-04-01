from logging import Logger
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.errors import UnauthorizedError
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.managers.token import TokenManager
from bot.usecases.record.delete import DeleteRecordUsecase


class DeleteRecordUsecaseImpl(DeleteRecordUsecase):
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

            self._record_api.delete(access_token, record_id)

            return UsecaseResult()
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id} - {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)
        except UnauthorizedError:
            if self._token_manager.with_tokens_refresh:
                return UsecaseResult(status=UsecaseStatus.UNAUTHORIZED)

            self._token_manager.with_tokens_refresh = True
            return self.__call__(telegram_id, record_id)
