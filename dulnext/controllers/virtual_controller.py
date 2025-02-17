from typing import Any, Dict, Optional

import frappe
from frappe.model.document import Document
from frappe.types import DF

from dulnext.exceptions import MissingDependencyError
from dulnext.models.comment import CommentController
from dulnext.models.like import LikeController
from dulnext.models.virtual_context import VirtualContext


class VirtualController(CommentController, LikeController, Document):
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
    _virtual_context: Optional[VirtualContext] = None

    def __init__(
        self,
        virtual_context: VirtualContext,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._virtual_context = virtual_context

    def get_virtual_context(self) -> VirtualContext:
        # Return the cached virtual model

        if not self._virtual_context:
            raise MissingDependencyError("Failed to get the Context")

        return self._virtual_context

    def map_enum(self) -> Optional[Dict[str, str]]:
        """
        This method maps enums and should return a dictionary of enums in the following format

        {
                        "ENUM1": "Enum description",
                        "ENUM2": "Another description"
        }

        The enum descriptions will be displayed in the Options Select Docfield,
        while the dictionary itself will be used when interacting with the database or REST API.
        """

        return None

    def get_liked_by(self):
        return self.get_likes()
