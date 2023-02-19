import json
from redis import Redis
from bot.models.tokens import Tokens


class TokenRepositoryRedis:
    def __init__(self, r_client: Redis):
        self._r_client = r_client

    def get_tokens_by_tg_id(self, telegram_id) -> Tokens:
        token_json = json.loads(self._r_client.get(telegram_id))
        
        return Tokens(
            access_token=token_json['access_token'],
            refresh_token=token_json['refresh_token']
        )

    def set_tokens(self, telegram_id, tokens: Tokens) -> None:
        tokens_json = json.dumps({
            telegram_id: tokens.access_token,
            telegram_id: tokens.refresh_token
        })

        self._r_client.set(telegram_id, tokens_json)
