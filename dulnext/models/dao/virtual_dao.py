from typing import Any, Dict

import frappe
from frappe.types import DF

from dulnext.typings.virtual_dao import VirtualActionResponse, VirtualCountResponse, VirtualFindResponse, VirtuaListResponse


# Please just use dict for AR
class VirtualDAO[T, AR]:
    """This class is used for retrieve or getting the data either from Database or API"""

    def get_item_count(self, filters: Dict[str, Any], pagination: Dict[str, Any]) -> VirtualCountResponse[AR]:
        """Get model instances counts."""
        raise NotImplementedError("Method not implemented.")

    def find_all(self, filters: Dict[str, Any], pagination: Dict[str, Any]) -> VirtuaListResponse[T, AR]:
        """Finds all model instances matching the given filters."""
        raise NotImplementedError("Method not implemented.")

    def destroy(self, name: str) -> VirtualActionResponse[T, AR]:
        """Deletes the current model instance from the database or API."""
        raise NotImplementedError("Method not implemented.")

    def update[U](self, name: str, new_data: U) -> VirtualActionResponse[T, AR]:
        """Updates the model instance in the database or API."""
        raise NotImplementedError("Method not implemented.")

    def insert[C](self, data: C) -> VirtualActionResponse[T, AR]:
        """Inserts the model instance in the database or API."""
        raise NotImplementedError("Method not implemented.")

    def find_one(
        self,
        filters: Dict[str, Any],
    ) -> VirtualFindResponse[T, Any]:
        """Finds a single model instance matching the given filters."""
        raise NotImplementedError("Method not implemented.")

    def find_one_by_pk(self, name: str) -> VirtualFindResponse[T, Any]:
        """Finds a model instance by its primary key."""
        raise NotImplementedError("Method not implemented.")

    def find_all_expensive(self) -> VirtuaListResponse[T, AR]:
        """Fetch all of the list data without pagination."""
        raise NotImplementedError("Method not implemented.")


class VirtualDocstatus:
    name: DF.Data
    doctype: DF.Data

    def __init__(self, name: DF.Data, doctype: DF.Data):
        self.name = name
        self.doctype = doctype

    def submit(self):
        """Mark docstatus of the model to submitted or '1'"""

        self.set_cached_property("docstatus", "1")

    def cancel(self):
        """Mark docstatus of the model to cancelled or '2'"""

        self.set_cached_property("docstatus", "2")

    def draft(self):
        """Mark docstatus of the model to cancelled or '0'"""

        self.set_cached_property("docstatus", "0")

    def is_submitted(self):
        """Determine if the model's docstatus is submitted."""

        return self.get_cached_property("docstatus") == "1"

    def is_draft(self):
        """Determine if the model's docstatus is draft."""

        return self.get_cached_property("docstatus") == "0"

    def is_cancelled(self):
        """Determine if the model's docstatus is cancelled."""

        return self.get_cached_property("docstatus") == "2"

    def get_cached_property(self, property: str):
        """Get cached properties on RedisWrapper."""

        property_key = f"{self.doctype}:{self.name}:{property}"

        return frappe.cache.get(property_key)

    def set_cached_property(self, property: str, value: str):
        """Set cached properties on RedisWrapper."""

        property_key = f"{self.doctype}:{self.name}:{property}"

        return frappe.cache.set(property_key, value)
