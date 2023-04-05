from pydantic import BaseModel


class Record(BaseModel):
    topic: str
    subtopic: str
    title: str
    content: str
    id: int = None
