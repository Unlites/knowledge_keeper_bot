import json
from redis import Redis
from bot.models.tokens import Tokens


class TokenRepositoryRedis:
    def __init__(self, r_client: Redis):
        self._r_client = r_client
        self.tokens_mark = "_tokens"

    def get_tokens(self, telegram_id) -> Tokens | None:
        token_str = self._r_client.get(f"{telegram_id}{self.tokens_mark}")
        if not token_str:
            return None

        token_json = json.loads(token_str)

        return Tokens(
            access_token=token_json["access_token"],
            refresh_token=token_json["refresh_token"],
        )

    def set_tokens(self, telegram_id, tokens: Tokens) -> None:
        self._r_client.set(f"{telegram_id}{self.tokens_mark}", tokens.json())
