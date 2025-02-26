import json
from typing import Any, Dict, Optional

import frappe
import inflection
from frappe.utils import now

from vrtnext.abc.virtual_model_mapper import VirtualModelMapper
from vrtnext.typings.document_metadata import DocumentMetadata
from vrtnext.utilities import get_nested, parse_docfield


class RestModelMapper(VirtualModelMapper):
    def map_doc_to_item(
        self,
        doc: Dict[str, Any],
        ignore_optional: bool = False,
    ) -> Dict[str, Any]:
        doc_fields = self.model_class.__annotations__.keys()
        item: Dict[str, Any] = {}

        for key in doc_fields:
            value = doc.get(key)

            docfieldmeta = parse_docfield(key)

            if value is None and ignore_optional or not docfieldmeta.is_can_mapped or not docfieldmeta.fieldname:
                continue

            if docfieldmeta.special_type == "idx" and isinstance(value, str):
                value = value.split(", ")

            item_key = docfieldmeta.fieldname

            if self.convention == "camelcase":
                item_key = inflection.camelize(item_key, False)

            traversed_keys = item_key.split("dot")
            ref = item

            for part in traversed_keys[:-1]:  # Traverse to the correct level
                if part not in ref:
                    ref[part] = {}
                ref = ref[part]

            ref[traversed_keys[-1]] = value  # Assign the final value

        return item

    def map_item_to_doc(self, item: Dict[str, Any], doc: Dict[str, Any], metadata: Optional[DocumentMetadata]) -> None:
        doc_fields = self.model_class.__annotations__.keys()

        for key in doc_fields:
            if self.convention == "camelcase":
                key = inflection.camelize(key, False)

            docfieldmeta = parse_docfield(key)

            if not docfieldmeta.is_can_mapped or not docfieldmeta.fieldname or not docfieldmeta.docfield_type:
                continue

            traversed_keys = docfieldmeta.fieldname.split("dot")
            ref = doc

            if self.convention == "camelcase":
                key = inflection.underscore(key)

            value = get_nested(item, traversed_keys)

            if docfieldmeta.fieldname == self.name_column:
                doc["name"] = value

            if docfieldmeta.special_type == "idx" and isinstance(value, list):
                value = ", ".join(value)

            ref[key] = value  # Assign the final value

        if metadata:
            doc["modified"] = metadata.modified
            doc["creation"] = metadata.creation
            doc["modified_by"] = metadata.modified_by
            doc["owner"] = metadata.owner
            doc["docstatus"] = metadata.docstatus
            doc["idx"] = metadata.idx
            doc["_user_tags"] = metadata._user_tags
            doc["_comments"] = metadata._comments
            doc["_assign"] = metadata._assign
            doc["_liked_by"] = metadata._liked_by
            if isinstance(metadata._comments, str):
                metadata._comments = json.loads(metadata._comments)
            doc["_comment_count"] = len(metadata._comments or [])
        else:
            doc["modified"] = now()
            doc["creation"] = now()
            doc["modified_by"] = frappe.session.user
            doc["owner"] = frappe.session.user
            doc["docstatus"] = 0
            doc["idx"] = 0
            doc["_user_tags"] = None
            doc["_comments"] = None
            doc["_assign"] = None
            doc["_liked_by"] = None
            doc["_comment_count"] = 0
