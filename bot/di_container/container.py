import punq
from logging import Logger
from redis import Redis
from bot.infrastructure.api.knowledge_keeper_api.implementation.record import (
    KnowledgeKeeperAPIRecordImpl,
)
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.usecases.managers.token_manager import TokenManager
from bot.usecases.implementation.record.create import CreateRecordUsecaseImpl
from bot.usecases.implementation.record.get_by_id import GetRecordByIdUsecaseImpl
from bot.usecases.record.create import CreateRecordUsecase
from bot.usecases.implementation.record.search_by_title import (
    SearchRecordsByTitleUsecaseImpl,
)
from bot.usecases.record.get_by_id import GetRecordByIdUsecase
from bot.usecases.record.search_by_title import SearchRecordsByTitleUsecase
from config.config import Config
from logger.logger import create_logger
from bot.infrastructure.repository.token_repo.implementation.token_redis import (
    TokenRepositoryRedis,
)
from bot.infrastructure.repository.token_repo.token_repo import TokenRepository
from bot.infrastructure.api.knowledge_keeper_api.implementation.auth import (
    KnowledgeKeeperAPIAuthImpl,
)
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.usecases.auth.sign_in import SignInUsecase
from bot.usecases.auth.sign_up import SignUpUsecase
from bot.usecases.implementation.auth.sign_in import SignInUsecaseImpl
from bot.usecases.implementation.auth.sign_up import SignUpUsecaseImpl


di_container = punq.Container()

di_container.register(Logger, instance=create_logger(Config.LOG_LEVEL))

r_client = Redis(
    host=Config.REDIS_HOST, password=Config.REDIS_PASSWORD, decode_responses=True
)

di_container.register(Redis, instance=r_client)
di_container.register(TokenRepository, TokenRepositoryRedis)

di_container.register(KnowledgeKeeperAPIAuth, KnowledgeKeeperAPIAuthImpl)
di_container.register(SignInUsecase, SignInUsecaseImpl)
di_container.register(SignUpUsecase, SignUpUsecaseImpl)

di_container.register(TokenManager)

di_container.register(KnowledgeKeeperAPIRecord, KnowledgeKeeperAPIRecordImpl)
di_container.register(CreateRecordUsecase, CreateRecordUsecaseImpl)
di_container.register(SearchRecordsByTitleUsecase, SearchRecordsByTitleUsecaseImpl)
di_container.register(GetRecordByIdUsecase, GetRecordByIdUsecaseImpl)
