import punq
from logging import Logger
from redis import Redis
from bot.cache.cache import Cache
from bot.cache.implementation.cache_redis import CacheRedis
from bot.infrastructure.api.knowledge_keeper_api.implementation.record import (
    KnowledgeKeeperAPIRecordImpl,
)
from bot.infrastructure.api.knowledge_keeper_api.record import KnowledgeKeeperAPIRecord
from bot.managers.token import TokenManager
from bot.managers.implementation.token import TokenManagerImpl
from bot.usecases.implementation.record.create import CreateRecordUsecaseImpl
from bot.usecases.implementation.record.delete import DeleteRecordUsecaseImpl
from bot.usecases.implementation.record.get_by_id import GetRecordByIdUsecaseImpl
from bot.usecases.implementation.record.get_subtopics import GetSubtopicsUsecaseImpl
from bot.usecases.implementation.record.get_topics import GetTopicsUsecaseImpl
from bot.usecases.implementation.record.update import UpdateRecordUsecaseImpl
from bot.usecases.record.create import CreateRecordUsecase
from bot.usecases.implementation.record.get_all import GetAllRecordsUsecaseImpl
from bot.usecases.record.delete import DeleteRecordUsecase
from bot.usecases.record.get_by_id import GetRecordByIdUsecase
from bot.usecases.record.get_subtopics import GetSubtopicsUsecase
from bot.usecases.record.get_topics import GetTopicsUsecase
from bot.usecases.record.get_all import GetAllRecordsUsecase
from bot.usecases.record.update import UpdateRecordUsecase
from config.config import Config
from logger.logger import create_logger
from bot.infrastructure.repository.implementation.token_redis import (
    TokenRepositoryRedis,
)
from bot.infrastructure.repository.token import TokenRepository
from bot.infrastructure.api.knowledge_keeper_api.implementation.auth import (
    KnowledgeKeeperAPIAuthImpl,
)
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth


di_container = punq.Container()

di_container.register(Logger, instance=create_logger(Config.LOG_LEVEL))

r_client = Redis(
    host=Config.REDIS_HOST,
    password=Config.REDIS_PASSWORD,
    decode_responses=True,
)

di_container.register(Redis, instance=r_client)
di_container.register(TokenRepository, TokenRepositoryRedis)

di_container.register(Cache, CacheRedis)

di_container.register(TokenManager, TokenManagerImpl)

di_container.register(KnowledgeKeeperAPIAuth, KnowledgeKeeperAPIAuthImpl)
di_container.register(KnowledgeKeeperAPIRecord, KnowledgeKeeperAPIRecordImpl)

di_container.register(CreateRecordUsecase, CreateRecordUsecaseImpl)
di_container.register(GetAllRecordsUsecase, GetAllRecordsUsecaseImpl)
di_container.register(GetRecordByIdUsecase, GetRecordByIdUsecaseImpl)
di_container.register(GetTopicsUsecase, GetTopicsUsecaseImpl)
di_container.register(GetSubtopicsUsecase, GetSubtopicsUsecaseImpl)
di_container.register(UpdateRecordUsecase, UpdateRecordUsecaseImpl)
di_container.register(DeleteRecordUsecase, DeleteRecordUsecaseImpl)
