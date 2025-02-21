from pydantic import BaseModel


class PostEntity(BaseModel):
    userId: int
    id: int
    title: str
    body: str
