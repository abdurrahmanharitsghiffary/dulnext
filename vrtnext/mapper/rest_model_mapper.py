from typing import Any, Dict

import inflection

from vrtnext.abc.virtual_model_mapper import VirtualModelMapper
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

    def map_item_to_doc(
        self,
        item: Dict[str, Any],
        doc: Dict[str, Any],
    ) -> None:
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

        doc["modified"] = doc.get("modified")
        doc["creation"] = doc.get("creation")
        doc["modified_by"] = doc.get("modified_by")
        doc["owner"] = doc.get("owner")
        doc["docstatus"] = doc.get("docstatus")
        doc["idx"] = doc.get("idx")
        doc["_user_tags"] = doc.get("_user_tags")
        doc["_comments"] = doc.get("_comments")
        doc["_assign"] = doc.get("_assign")
        doc["_liked_by"] = doc.get("_liked_by")
