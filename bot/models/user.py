from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    id: int = None
