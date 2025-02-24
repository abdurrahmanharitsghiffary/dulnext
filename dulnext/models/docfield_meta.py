from typing import Optional

from pydantic import BaseModel


class DocfieldMeta(BaseModel):
    fieldname: Optional[str]
    docfield_type: Optional[str]
    special_type: Optional[str]
    is_can_mapped: bool

    def get_docfield(self) -> str:
        special_type = ""
        if self.special_type:
            special_type = f"spq{self.special_type}"

        return f"dfq{self.docfield_type}{special_type}{self.fieldname}"
