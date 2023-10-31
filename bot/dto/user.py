from pydantic import BaseModel, Field


class RequestUserDTO(BaseModel):
    username: str = Field(min_length=2, max_length=20, default="")
    password: str = Field(min_length=6, max_length=16, default="")

    class Config:
        validate_assignment = True