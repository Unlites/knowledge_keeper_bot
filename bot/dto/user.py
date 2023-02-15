from pydantic import Field, validator
from pydantic.dataclasses import dataclass

@dataclass
class UserSignInDTO:
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=6, max_length=20)

@dataclass
class UserSignUpDTO:
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    confirm_password: str = ""

    @validator("confirm_password")
    def passwords_matching(cls, value, values, **kwargs):
        if value != values["password"]:
            raise ValueError("passwords do not match")
        return value
    