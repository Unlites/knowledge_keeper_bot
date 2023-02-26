from logging import Logger
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus
from bot.dto.record import CreateRecordDTO
from bot.infrastructure.api.errors import KnowledgeKeeperAPIError
from bot.infrastructure.api.errors import KnowledgeKeeperAPIUnauthorized
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.infrastructure.repository.token_repo.token_repo import TokenRepository
from bot.models.record import Record
from bot.usecases.record.create import CreateRecordUsecase


class CreateRecordUsecaseImpl(CreateRecordUsecase):
    def __init__(
        self,
        logger: Logger,
        record_api: KnowledgeKeeperAPIRecord,
        auth_api: KnowledgeKeeperAPIAuth,
        token_repo: TokenRepository
    ) -> None:
        self._logger = logger
        self._record_api = record_api
        self._auth_api = auth_api
        self._token_repo = token_repo
        self._tokens_refresh_attempted = False
        self._with_tokens_refresh = False

    def __call__(self, telegram_id, record_dto: CreateRecordDTO) -> UsecaseResult:
        try:
            tokens = self._token_repo.get_tokens_by_tg_id(telegram_id)

            if not tokens:
                return UsecaseResult(status=UsecaseStatus.UNAUTHORIZED)
            
            if self._with_tokens_refresh:
                if self._tokens_refresh_attempted:
                    return UsecaseResult(status=UsecaseStatus.UNAUTHORIZED)
                
                self._tokens_refresh_attempted = True
                tokens = self._auth_api.refresh(tokens.refresh_token)
                self._token_repo.set_tokens(telegram_id, tokens)
            
            record = Record(
                topic=record_dto.topic,
                title=record_dto.title,
                content=record_dto.content,
            )
            self._record_api.create_record(tokens.access_token, record)
            return UsecaseResult()
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id} - {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)
        except KnowledgeKeeperAPIUnauthorized:
            self._with_tokens_refresh = True
            return self.__call__(telegram_id, record_dto)