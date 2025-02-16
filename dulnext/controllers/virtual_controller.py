from typing import Any, Dict, Optional

import frappe
from frappe.model.document import Document
from frappe.types import DF

from dulnext.exceptions import MissingDependencyError
from dulnext.models.comment import CommentController
from dulnext.models.filterable import Filterable
from dulnext.models.like import LikeController
from dulnext.models.paginated import Paginated
from dulnext.models.virtual_dao import VirtualDAO


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
    _virtual_dao: Optional[VirtualDAO] = None
    _filterable: Optional[Filterable] = None
    _paginated: Optional[Paginated] = None

    def __init__(
        self,
        virtual_dao: VirtualDAO,
        paginated: Paginated,
        filterable: Filterable,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._filterable = filterable
        self._paginated = paginated
        self._virtual_dao = virtual_dao

    def get_filter_mapper(self) -> Filterable:
        # Return the cached virtual model

        if not self._filterable:
            raise MissingDependencyError("Failed to get the Filterable")

        return self._filterable

    def get_pagination_mapper(self) -> Paginated:
        # Return the cached virtual model

        if not self._paginated:
            raise MissingDependencyError("Failed to get the Paginated")

        return self._paginated

    def get_virtual_dao(self) -> VirtualDAO:
        # Return the cached virtual model

        if not self._virtual_dao:
            raise MissingDependencyError("Failed to get the VirtualDAO")

        return self._virtual_dao

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
