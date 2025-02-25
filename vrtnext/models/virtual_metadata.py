import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Optional

import frappe
from frappe.utils.redis_wrapper import RedisWrapper

from vrtnext.typings.enums import RedisKey


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


class VirtualDocumentMetadata:
    def find(self, doctype: str, name: str) -> DocumentMetadata | None:
        """Find one metadata."""
        raise NotImplementedError("Method not implemented.")


class RedisDocumentMetadata(VirtualDocumentMetadata):
    def find(self, doctype: str, name: str) -> DocumentMetadata | None:
        cache = RedisWrapper()

        response = cache.get(f"{RedisKey.VirtualMetadata.value}::{frappe.scrub(doctype)}:{name}")

        if response:
            data = {
                "modified": None,
                "creation": None,
                "owner": None,
                "modified_by": None,
                "docstatus": None,
                "idx": None,
                "_user_tags": None,
                "_liked_by": None,
                "_comments": None,
                "_assign": None,
                **json.loads(response),
            }

            return DocumentMetadata(**data)

        return None

    def update_meta(self, doctype: str, name: str, key: str, value: Any) -> None:
        cache = RedisWrapper()

        response = self.find(doctype, name)

        if response:
            response.__setattr__(key, value)

            cache.set(f"{RedisKey.VirtualMetadata.value}::{frappe.scrub(doctype)}:{name}", json.dumps(response.__dict__))

    def set(self, doctype: str, name: str, value: DocumentMetadata):
        cache = RedisWrapper()

        cache.set(f"{RedisKey.VirtualMetadata.value}::{frappe.scrub(doctype)}:{name}", json.dumps(value.__dict__))


if __name__ == "__main__":
    redis_virtual_metadata = RedisDocumentMetadata()

    item = redis_virtual_metadata.find("Post JSON Placeholder", "lolers")

    redis_virtual_metadata.set(
        "Post JSON Placeholder",
        "lolers",
        DocumentMetadata(
            _user_tags="",
            _liked_by="",
            _comments="",
            _assign="",
            modified=datetime(2024, 3, 15).isoformat(),
            modified_by="Administrator",
            creation=datetime(2024, 3, 15).isoformat(),
            owner="Administrator",
            docstatus=0,
            idx=0,
        ),
    )

    print(f"Item: {item}")

    redis_virtual_metadata.update_meta("Post JSON Placeholder", "lolers", "modified", "2025-04-13")

    item = redis_virtual_metadata.find("Post JSON Placeholder", "lolers")

    print(f"Item: {item}")
