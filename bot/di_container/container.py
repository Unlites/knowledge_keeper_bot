import punq
from logging import Logger
from logger.logger import logger
from bot.infrastructure.api.knowledge_keeper_api.implementation.auth import KnowledgeKeeperAPIAuthImpl
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.usecases.implementation.sign_in import SignInUseCaseImpl
from bot.usecases.auth.sign_in import SignInUseCase


di_container = punq.Container()

di_container.register(Logger, instance=logger)

di_container.register(KnowledgeKeeperAPIAuth, KnowledgeKeeperAPIAuthImpl)
di_container.register(SignInUseCase, SignInUseCaseImpl)

