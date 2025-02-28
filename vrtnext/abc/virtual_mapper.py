from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional

from vrtnext.typings.document_metadata import DocumentMetadata


class VirtualMapper(ABC):
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

    @abstractmethod
    def map_doc_to_item(
        self,
        doc: Dict[str, Any],
        ignore_optional: bool = False,
    ) -> Dict[str, Any]:
        """Map doc to item which is displayed as List"""
        pass

    @abstractmethod
    def map_item_to_doc(
        self,
        item: Dict[str, Any],
        doc: Dict[str, Any],
        metadata: Optional[DocumentMetadata],
    ) -> None:
        """Map item to doc which is displayed as List"""
        pass
