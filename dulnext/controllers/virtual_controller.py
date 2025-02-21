from typing import Dict, Optional

from frappe.model.document import Document

from dulnext.models.like import LikeController


class VirtualController(Document):
    """
    VirtualController is an abstract base class that serves as a contract for derived classes.
    Classes inheriting from VirtualController, such as RestController and DatabaseController.
    """

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
        return LikeController().get_likes()
