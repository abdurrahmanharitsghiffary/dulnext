from typing import Any, Dict, Literal


class VirtualMapper:
    """Base class for mapping document"""

    name_column: str
    convention: Literal["camelcase", "snakecase"]

    def __init__(
        self,
        convention: Literal["camelcase", "snakecase"] = "snakecase",
        name_column: str = "id",
    ):
        self.convention = convention
        self.name_column = name_column

    def map_doc_to_item(
        self,
        doc: Dict[str, Any],
        ignore_optional: bool = False,
    ) -> Dict[str, Any]:
        """Map doc to item which is displayed as List"""
        raise NotImplementedError("Method not implemented.")

    def map_item_to_doc(
        self,
        item: Dict[str, Any],
        doc: Dict[str, Any],
    ) -> None:
        """Map item to doc which is displayed as List"""
        raise NotImplementedError("Method not implemented.")
