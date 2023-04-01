from pydantic import BaseModel


class UserCache(BaseModel):
    found_topics: list[dict] | None
