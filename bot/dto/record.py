from pydantic import BaseModel, Field


class CreateRecordDTO(BaseModel):
    topic: str = Field(min_length=1, max_length=100, default="")
    title: str = Field(min_length=1, max_length=255, default="")
    content: str = Field(min_lenght=1, max_length=3000, default="")

    class Config:
        validate_assignment = True


class GetRecordDTO(BaseModel):
    id: int
    topic: str
    title: str
    content: str
