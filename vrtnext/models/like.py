import frappe
from frappe.types import DF


class LikeController:
    """Class for controlling like on Virtual Doctype"""

    doctype: DF.Data
    name: DF.Data | None

    def __init__(self, name: DF.Data, doctype: DF.Data):
        self.name = name
        self.doctype = doctype

    def get_likes(self):
        try:
            filters = [
                ["reference_name", "=", self.name],
                ["comment_type", "=", "Like"],
            ]

            return frappe.db.get_list("Comment", filters=filters, order_by="modified desc")

        except Exception:
            return []

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
