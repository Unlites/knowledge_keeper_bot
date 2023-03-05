from pydantic import BaseModel, Field, validator


class UserSignInDTO(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=6, max_length=20)


class UserSignUpDTO(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    confirm_password: str = Field(min_length=1)

    @validator("confirm_password")
    def passwords_matching(cls, value, values, **kwargs):
        if value != values.get("password"):
            raise ValueError("passwords do not match")
        return value
