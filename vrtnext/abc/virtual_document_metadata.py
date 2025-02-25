from abc import ABC, abstractmethod
from typing import Any

from vrtnext.typings.document_metadata import DocumentMetadata


class VirtualDocumentMetadata(ABC):
    @abstractmethod
    def find(self, doctype: str, name: str) -> DocumentMetadata | None:
        """Find one metadata."""
        pass

    @abstractmethod
    def update_meta(self, doctype: str, name: str, key: str, value: Any) -> None:
        """Should update one value of DocumentMetadata."""
        pass

    @abstractmethod
    def set(self, doctype: str, name: str, value: DocumentMetadata) -> None:
        """Set DocumentMetadata."""
        pass
