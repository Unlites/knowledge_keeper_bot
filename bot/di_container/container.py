import punq
from logging import Logger
from logger.logger import logger
from bot.infrastructure.api.knowledge_keeper_api.implementation.auth import KnowledgeKeeperAPIAuthImpl
from bot.infrastructure.api.knowledge_keeper_api.auth import KnowledgeKeeperAPIAuth
from bot.usecases.implementation.sign_in import SignInUsecaseImpl
from bot.usecases.auth.sign_in import SignInUsecase
from bot.usecases.auth.sign_up import SignUpUsecase
from bot.usecases.implementation.sign_up import SignUpUsecaseImpl


di_container = punq.Container()

di_container.register(Logger, instance=logger)

di_container.register(KnowledgeKeeperAPIAuth, KnowledgeKeeperAPIAuthImpl)
di_container.register(SignInUsecase, SignInUsecaseImpl)
di_container.register(SignUpUsecase, SignUpUsecaseImpl)

