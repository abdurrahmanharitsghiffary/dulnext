import json
from typing import Any

import frappe
from frappe.utils import now

from vrtnext.abc.virtual_document_metadata import VirtualDocumentMetadata
from vrtnext.typings.document_metadata import DocumentMetadata
from vrtnext.typings.enums import CacheKey


class RedisDocumentMetadata(VirtualDocumentMetadata):
    """Class for handle the storing metadata into redis storage."""

    def find(self, doctype: str, name: str) -> DocumentMetadata | None:
        cache = frappe.cache()
        response = cache.get(f"{CacheKey.VirtualDocumentMetadata.value}::{frappe.scrub(doctype)}:{name}")

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
        cache = frappe.cache()
        response = self.find(doctype, name)

        if response:
            response.__setattr__(key, value)
            response.__setattr__("modified", now())
            response.__setattr__("modified_by", frappe.session.get("user", "Anonymous"))
            cache_key = f"{CacheKey.VirtualDocumentMetadata.value}::{frappe.scrub(doctype)}:{name}"

            cache.set(cache_key, json.dumps(response.__dict__))

    def update_timestamp(
        self,
        doctype: str,
        name: str,
    ):
        cache = frappe.cache()
        response = self.find(doctype, name)

        if response:
            response.__setattr__("modified", now())
            response.__setattr__("modified_by", frappe.session.get("user", "Anonymous"))
            cache_key = f"{CacheKey.VirtualDocumentMetadata.value}::{frappe.scrub(doctype)}:{name}"

            cache.set(cache_key, json.dumps(response.__dict__))

    def set(self, doctype: str, name: str, value: DocumentMetadata) -> None:
        cache = frappe.cache()
        default_meta = self.get_default_doc_metadata()

        value.creation = now()
        value.modified = now()
        value.modified_by = frappe.session.get("user", "Anonymous")
        value.owner = frappe.session.get("user", "Anonymous")

        merged_meta = {**default_meta.__dict__, **value.__dict__}
        cache_key = f"{CacheKey.VirtualDocumentMetadata.value}::{frappe.scrub(doctype)}:{name}"

        cache.set(cache_key, json.dumps(merged_meta))

    def find_or_save(self, doctype: str, name: str) -> DocumentMetadata | None:
        result = self.find(doctype, name)
        if not result:
            value = self.get_default_doc_metadata()
            self.set(doctype, name, value)

        return result

    def get_default_doc_metadata(self) -> DocumentMetadata:
        data = {
            "modified": self.get_default_user(),
            "creation": now(),
            "owner": self.get_default_user(),
            "modified_by": now(),
            "docstatus": 0,
            "idx": 0,
            "_user_tags": None,
            "_liked_by": None,
            "_comments": None,
            "_assign": None,
        }

        return DocumentMetadata(**data)

    def get_default_user(self) -> str:
        return frappe.session.get("user", "Anonymous")
