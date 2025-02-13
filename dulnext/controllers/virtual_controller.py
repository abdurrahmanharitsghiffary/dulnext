from typing import Any, Dict, Optional

import frappe
from frappe.model.document import Document
from frappe.types import DF

from dulnext.exceptions import NotFoundException
from dulnext.mixins.singleton import SingletonMixin


class VirtualModel(SingletonMixin):
    """All Virtual Doctype should derive this class"""

    # Primary Key of the model
    doctype: Optional[str] = None
    name: Optional[str] = None

    def __init__(self, doctype: str, name: str):
        self.doctype = doctype
        self.name = name

    @staticmethod
    def find_all(*args, **kwargs):
        """Finds all model instances matching the given filters."""
        raise NotImplementedError("Method not implemented.")

    def destroy(self):
        """Deletes the current model instance from the database or API."""
        raise NotImplementedError("Method not implemented.")

    def save(self, *args, **kwargs):
        """Inserts or updates the model instance in the database or API."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def find_one(*args, **kwargs):
        """Finds a single model instance matching the given filters."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def find_one_by_pk(id):
        """Finds a model instance by its primary key."""
        raise NotImplementedError("Method not implemented.")

    def submit(self):
        """Mark docstatus of the model to submitted or '1'"""
        if self.name:
            self.set_cached_property("docstatus", "1")
        else:
            raise NotFoundException(
                f"Entity {self.doctype} with id: {self.name} not found."
            )

    def cancel(self):
        """Mark docstatus of the model to cancelled or '2'"""
        if self.name:
            self.set_cached_property("docstatus", "2")

        else:
            raise NotFoundException(
                f"Entity {self.doctype} with id: {self.name} not found."
            )

    def draft(self):
        """Mark docstatus of the model to cancelled or '0'"""

        if self.name:
            self.set_cached_property("docstatus", "0")

        else:
            raise NotFoundException(
                f"Entity {self.doctype} with id: {self.name} not found."
            )

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


class PaginationOptions:
    page_length: str
    start: str


class Filterable:
    @staticmethod
    def filters_mapper(filters: Dict[str, Any]):
        """Depends on the database type you should map the filters by yourself, for example we provide mapper for postgresql database, while using rest api we must define it by ourself because rest api always have different response structure"""
        pass


class Paginated:
    @staticmethod
    def pagination_mapper(pagination: PaginationOptions):
        """Mapper method for pagination passed by frappe us"""
        pass


class CommentController:
    """Class for controlling comment on Virtual Doctype"""

    doctype: Optional[str] = None
    name: Optional[str] = None
    fieldname: Optional[str] = None
    value: Optional[str] = None

    def __init__(self, name: str, fieldname: str, doctype):
        self.name = name
        self.fieldname = fieldname
        self.doctype = doctype

    def get(self):
        filters = [
            ["reference_name", "=", self.name],
            ["content", "=", "Comment"],
        ]

        return frappe.db.get_list("Comment", filters=filters, order_by="modified desc")

    def append_value(self, new_value: str):
        comment_doc = frappe.get_doc(
            {
                "doctype": "Comment",
                "comment_type": "Comment",
                "content": new_value,
                "reference_doctype": self.doctype,
                "reference_name": self.name,
            }
        )

        comment_doc.insert(ignore_permissions=True)


class LikeController:
    """Class for controlling like on Virtual Doctype"""

    doctype: Optional[str] = None
    name: Optional[str] = None
    fieldname: Optional[str] = None
    value: Optional[str] = None

    def __init__(self, name: str, fieldname: str, doctype):
        self.name = name
        self.fieldname = fieldname
        self.doctype = doctype

    def get(self):
        filters = [
            ["reference_name", "=", self.name],
            ["comment_type", "=", "Like"],
        ]

        return frappe.db.get_list("Comment", filters=filters, order_by="modified desc")

    def like(self):
        comment_doc = frappe.get_doc(
            {
                "doctype": "Comment",
                "comment_type": "Liked",
                "content": "Liked",
                "reference_doctype": self.doctype,
                "reference_name": self.name,
            }
        )

        comment_doc.insert(ignore_permissions=True)


class VirtualController(
    Filterable, Paginated, CommentController, LikeController, Document
):
    """
    VirtualController is an abstract base class that serves as a contract for derived classes.
    Classes inheriting from VirtualController, such as RestController and DatabaseController.
    """

    doctype: DF.Data
    name: DF.Data | None
    flags: frappe._dict[str, Any]
    owner: DF.Link
    creation: DF.Datetime
    modified: DF.Datetime
    modified_by: DF.Link
    idx: DF.Int
    model_creator: Optional[VirtualModel] = None

    def __init__(self, model_creator: VirtualModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_creator = model_creator

    def get_virtual_model(self):
        # Return the cached virtual model
        return self.model_creator(self.doctype, self.name)

    def validate(disable_select_validation=False):
        pass

    def map_enum(self):
        """
        This method maps enums and should return a dictionary of enums in the following format

        {
            "ENUM1": "Enum description",
            "ENUM2": "Another description"
        }

        The enum descriptions will be displayed in the Options Select Docfield,
        while the dictionary itself will be used when interacting with the database or REST API.
        """
        pass
