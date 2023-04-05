import json
from redis import Redis
from bot.cache.user import UserCache


class CacheRedis:
    def __init__(self, r_client: Redis):
        self._r_client = r_client
        self.cache_mark = "_cache"

    def get_user_cache(self, telegram_id) -> UserCache:
        cache_str = self._r_client.get(f"{telegram_id}{self.cache_mark}")
        if not cache_str:
            return UserCache()

        cache = json.loads(cache_str)

        return UserCache(
            found_topics=cache.get("found_topics"),
            found_subtopics=cache.get("found_subtopics"),
        )

    def set_user_cache(self, telegram_id, cache: UserCache) -> None:
        self._r_client.set(f"{telegram_id}{self.cache_mark}", cache.json())
