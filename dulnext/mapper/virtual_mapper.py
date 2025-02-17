from typing import Any, Dict


class VirtualMapper:
    """Base class for mapping document"""

    def map_doc_to_item(self, item: Dict[str, Any], ignore_optional: bool) -> Dict[str, Any]:
        """Map doc to item which is displayed as List"""
        raise NotImplementedError("Method not implemented.")

    def map_item_to_doc(self, item: Dict[str, Any], doc: Dict[str, Any], ignore_optional: bool) -> Dict[str, Any]:
        """Map item to doc which is displayed as List"""
        raise NotImplementedError("Method not implemented.")
