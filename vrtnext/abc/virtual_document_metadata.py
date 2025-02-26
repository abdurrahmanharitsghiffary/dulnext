from abc import ABC, abstractmethod
from typing import Any

from vrtnext.typings.document_metadata import DocumentMetadata


class VirtualDocumentMetadata(ABC):
    def find(self, doctype: str, name: str) -> DocumentMetadata | None:
        """Find one metadata. if this method does not implemented it will use the map_doc_metadata instead"""
        raise NotImplementedError()

    @abstractmethod
    def update_meta(self, doctype: str, name: str, key: str, value: Any) -> None:
        """Should update one value of DocumentMetadata."""
        pass

    @abstractmethod
    def set(self, doctype: str, name: str, value: DocumentMetadata) -> None:
        """Set DocumentMetadata."""
        pass
