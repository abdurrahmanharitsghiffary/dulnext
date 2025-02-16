from pydantic import BaseModel


class PaginationOptions(BaseModel):
    page_length: str
    start: str
