from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class DocumentMetadata:
    modified: Optional[str]
    creation: str
    owner: str
    modified_by: Optional[str]
    docstatus: Literal[0, 1, 2]
    idx: int
    _user_tags: str
    _liked_by: str
    _comments: str
    _assign: str
