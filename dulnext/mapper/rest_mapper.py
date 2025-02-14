from typing import Any, Dict

from dulnext.mixins.singleton import SingletonMixin


class RestMapper(SingletonMixin):
    def map_rest_to_doc(self, rest: Dict[str, Any], doc: Dict[str, Any], ignore_optional=False) -> Dict[str, Any]:
        """Map the api response to doctype"""

        def process_key_value(key: str, value: Any, parent_key: str = ""):
            """Recursively process nested fields and apply transformation rules."""
            full_key = f"{parent_key}dot{key}" if parent_key else key

            if isinstance(value, dict):
                # Process nested dictionary
                for sub_key, sub_value in value.items():
                    process_key_value(sub_key, sub_value, full_key)
            elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                # Convert array of strings to a comma-separated string with 'idxspq' prefix
                doc[f"dfqidxsp{full_key}"] = ",".join(value)
            else:
                # Normal field mapping with 'dfq' prefix
                doc[f"dfq{full_key}"] = value

        for key, value in rest.items():
            if ignore_optional and value is None:
                continue
            process_key_value(key, value)

        return doc

    def map_doc_to_rest(self, doc: Dict[str, Any], ignore_optional=False) -> Dict[str, Any]:
        """Map the doctype to api response"""

        original_doc: Dict[str, Any] = {}

        for key, value in doc.items():
            if (ignore_optional and value is None) or not key.startswith("df"):
                continue

            if key.startswith("dfqidxsp"):
                # Convert back to an array of strings
                clean_key = key[len("dfqidxsp") :]
                value = value.split(",")  # Convert back to list
            elif key.startswith("dfq"):
                # Remove 'dfq' prefix
                clean_key = key[len("dfq") :]
            else:
                clean_key = key  # Just in case there's a key that doesn't match the pattern

            keys = clean_key.split("dot")  # Handle nested keys
            ref = original_doc

            for part in keys[:-1]:  # Traverse to the correct level
                if part not in ref:
                    ref[part] = {}
                ref = ref[part]

            ref[keys[-1]] = value  # Assign the final value

        return original_doc
