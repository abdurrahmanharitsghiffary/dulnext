from typing import Any, Dict, Literal

import inflection
from deprecated import deprecated

from vrtnext.mapper.virtual_mapper import VirtualMapper


def process_key_value(key: str, value: Any, doc: Dict[str, Any], parent_key: str = ""):
    """Recursively process nested fields and apply transformation rules."""
    full_key = f"{parent_key}dot{key}" if parent_key else key

    is_value_dict = isinstance(value, dict)
    is_value_list_of_str = isinstance(value, list) and all(isinstance(item, str) for item in value)

    if is_value_dict:
        # Process nested dictionary
        for sub_key, sub_value in value.items():
            process_key_value(sub_key, sub_value, doc, full_key)
    elif is_value_list_of_str:
        # Convert array of strings to a comma-separated string with 'dfqidxsp' prefix
        doc[f"dfqidxsp{full_key}"] = ",".join(value)
    else:
        # Normal field mapping with 'dfq' prefix
        doc[f"dfq{full_key}"] = value


@deprecated(version="1.0.0", reason="You should use RestModelMapper instead")
class RestMapper(VirtualMapper):
    def __init__(
        self,
        convention: Literal["snakecase", "camelcase"] = "snakecase",
        name_column: str = "id",
    ):
        super().__init__(convention, name_column)

    def map_item_to_doc(
        self,
        item: Dict[str, Any],
        doc: Dict[str, Any],
        ignore_optional: bool = False,
    ) -> None:
        """Map the api response to doctype"""

        for key, value in item.items():
            snake_cased_key = key

            if self.convention == "camelcase":
                snake_cased_key = inflection.underscore(key)

            if ignore_optional and value is None:
                continue

            if snake_cased_key == self.name_column:
                doc["name"] = value

            process_key_value(snake_cased_key, value, doc)

    def map_doc_to_item(
        self,
        doc: Dict[str, Any],
        ignore_optional=False,
    ) -> Dict[str, Any]:
        """Map the doctype to api response"""
        original_doc: Dict[str, Any] = {}

        for key, value in doc.items():
            if (ignore_optional and value is None) or not key.startswith("dfq"):
                continue

            if key == self.name_column:
                original_doc["name"] = value

            if key.startswith("dfqidxsp"):
                # Convert back to an array of strings
                clean_key = key[len("dfqidxsp") :]
                value = value.split(",")  # Convert back to list
            elif key.startswith("dfq"):
                # Remove 'dfq' prefix
                clean_key = key[len("dfq") :]
            else:
                clean_key = key  # Just in case there's a key that doesn't match the pattern

            if self.convention == "camelcase":
                clean_key = inflection.camelize(clean_key, False)

            keys = clean_key.split("dot")  # Handle nested keys
            ref = original_doc

            for part in keys[:-1]:  # Traverse to the correct level
                if part not in ref:
                    ref[part] = {}
                ref = ref[part]

            ref[keys[-1]] = value  # Assign the final value

        return original_doc
