from abc import ABC, abstractmethod
from bot.cache.user import UserCache


class Cache(ABC):
    @abstractmethod
    def get_user_cache(self, telegram_id) -> UserCache | None:
        pass

    @abstractmethod
    def set_user_cache(self, telegram_id, cache: UserCache) -> None:
        pass
