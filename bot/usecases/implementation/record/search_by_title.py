from logging import Logger
from bot.dto.record import GetRecordDTO
from bot.dto.usecase_result import UsecaseResult, UsecaseStatus
from bot.infrastructure.api.errors import (
    KnowledgeKeeperAPIError,
    KnowledgeKeeperAPIUnauthorized,
)
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.infrastructure.repository.token_repo.token_repo import TokenRepository
from bot.usecases.record.search_by_title import SearchByTitleUsecase


class SearchByTitleUsecaseImpl(SearchByTitleUsecase):
    def __init__(
        self,
        logger: Logger,
        record_api: KnowledgeKeeperAPIRecord,
        auth_api: KnowledgeKeeperAPIAuth,
        token_repo: TokenRepository,
    ) -> None:
        self._logger = logger
        self._record_api = record_api
        self._auth_api = auth_api
        self._token_repo = token_repo
        self._tokens_refresh_attempted = False
        self._with_tokens_refresh = False

    def __call__(self, telegram_id, title, limit, offset) -> UsecaseResult:
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

            records = self._record_api.search_by_title(
                tokens.access_token, title, limit, offset
            )

            record_dtos = []
            for record in records:
                record_dtos.append(
                    GetRecordDTO(
                        id=record.id,
                        topic=record.topic,
                        title=record.title,
                        content=record.content,
                    )
                )
            return UsecaseResult(record_dtos)
        except KnowledgeKeeperAPIError as e:
            self._logger.error(f"{telegram_id} - {e.detail}")
            return UsecaseResult(e, status=UsecaseStatus.FAILURE)
        except KnowledgeKeeperAPIUnauthorized:
            self._with_tokens_refresh = True
            return self.__call__(telegram_id, title, limit, offset)
