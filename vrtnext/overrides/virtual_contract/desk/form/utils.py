import json
from typing import TYPE_CHECKING

import frappe
import frappe.desk.form.load
import frappe.desk.form.meta
from frappe import _
from frappe.core.doctype.file.utils import extract_images_from_html
from frappe.desk.form.document_follow import follow_document

from vrtnext.common.document_metadata.redis_document_metadata import (
    RedisDocumentMetadata,
)

if TYPE_CHECKING:
    from frappe.core.doctype.comment.comment import Comment


def update_comment_meta(doctype: str, name: str):
    redis_doc_meta = RedisDocumentMetadata()

    filters = [
        ["reference_name", "=", name],
        ["comment_type", "=", "Comment"],
        ["reference_doctype", "=", doctype],
    ]

    comments = frappe.db.get_list(
        "Comment", fields=["content", "comment_by", "name"], filters=filters
    )

    print(f"Comments: {comments}")

    cached_comments = [
        {
            "comment": comment.get("content", ""),
            "by": comment.get("comment_by"),
            "name": comment.get("name"),
        }
        for comment in comments
    ]

    redis_doc_meta.update_meta(
        doctype, name, "_comments", json.dumps(cached_comments)
    )


@frappe.whitelist(methods=["POST", "PUT"])
def add_comment(
    reference_doctype: str,
    reference_name: str,
    content: str,
    comment_email: str,
    comment_by: str,
) -> "Comment":
    """Allow logged user with permission to read document to add a comment"""
    reference_doc = frappe.get_doc(reference_doctype, reference_name)
    reference_doc.check_permission()

    comment = frappe.new_doc("Comment")
    comment.update(
        {
            "comment_type": "Comment",
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "comment_email": comment_email,
            "comment_by": comment_by,
            "content": extract_images_from_html(
                reference_doc, content, is_private=True
            ),
        }
    )
    comment.insert(ignore_permissions=True)

    if frappe.get_cached_value(
        "User", frappe.session.user, "follow_commented_documents"
    ):
        follow_document(
            comment.reference_doctype,
            comment.reference_name,
            frappe.session.user,
        )

    is_virtual_doctype = frappe.get_meta(reference_doctype).is_virtual

    if is_virtual_doctype:
        update_comment_meta(reference_doctype, reference_name)

    return comment


@frappe.whitelist()
def update_comment(name, content):
    """allow only owner to update comment"""
    doc = frappe.get_doc("Comment", name)

    if frappe.session.user not in ["Administrator", doc.owner]:
        frappe.throw(
            _("Comment can only be edited by the owner"), frappe.PermissionError
        )

    if doc.reference_doctype and doc.reference_name:
        reference_doc = frappe.get_doc(
            doc.reference_doctype, doc.reference_name
        )
        reference_doc.check_permission()

        doc.content = extract_images_from_html(
            reference_doc, content, is_private=True
        )
    else:
        doc.content = content

    is_virtual_doctype = frappe.get_meta(doc.reference_doctype).is_virtual

    if is_virtual_doctype:
        update_comment_meta(doc.reference_doctype, doc.reference_name)

    doc.save(ignore_permissions=True)
