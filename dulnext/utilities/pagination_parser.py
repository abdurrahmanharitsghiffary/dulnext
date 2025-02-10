import math

from pydantic import BaseModel


class ParsePaginationReturn(BaseModel):
    per_page: int
    page: int


# When we click filters in frappe they will not pass the page_length so its not available or None


def parse_pagination(args):
    per_page = int(args.get("page_length", 20))
    start = int(args.get("start", 0))
    page = math.ceil(start / per_page) + 1

    return ParsePaginationReturn(page=page, per_page=per_page)
