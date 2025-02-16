from typing import Optional

import frappe


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

    def get_comments(self):
        filters = [
            ["reference_name", "=", self.name],
            ["content", "=", "Comment"],
        ]

        return frappe.db.get_list("Comment", filters=filters, order_by="modified desc")

    def append_comment(self, new_comment: str):
        comment_doc = frappe.get_doc(
            {
                "doctype": "Comment",
                "comment_type": "Comment",
                "content": new_comment,
                "reference_doctype": self.doctype,
                "reference_name": self.name,
            }
        )

        comment_doc.insert(ignore_permissions=True)
