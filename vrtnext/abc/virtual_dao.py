from abc import ABC, abstractmethod
from typing import Any, Dict

from vrtnext.typings.virtual_dao import (
    VirtualActionResponse,
    VirtualCountResponse,
    VirtualFindResponse,
    VirtuaListResponse,
)


class VirtualDAO[T, AR](ABC):
    """This class is used for retrieve or getting the data either from Database or API"""

    @abstractmethod
    def get_item_count(
        self, filters: Dict[str, Any], pagination: Dict[str, Any]
    ) -> VirtualCountResponse[AR]:
        """Get model instances counts."""
        pass

    @abstractmethod
    def find_all(
        self, filters: Dict[str, Any], pagination: Dict[str, Any]
    ) -> VirtuaListResponse[T, AR]:
        """Finds all model instances matching the given filters. should return all of the list data if used in ClientSideContext"""
        pass

    @abstractmethod
    def destroy(self, name: str) -> VirtualActionResponse[T, AR]:
        """Deletes the current model instance from the database or API."""
        pass

    @abstractmethod
    def update[U](self, name: str, new_data: U) -> VirtualActionResponse[T, AR]:
        """Updates the model instance in the database or API."""
        pass

    @abstractmethod
    def insert[C](self, data: C) -> VirtualActionResponse[T, AR]:
        """Inserts the model instance in the database or API."""
        pass

    @abstractmethod
    def find_one(
        self,
        filters: Dict[str, Any],
    ) -> VirtualFindResponse[T, Any]:
        """Finds a single model instance matching the given filters."""
        pass

    @abstractmethod
    def find_one_by_pk(self, name: str) -> VirtualFindResponse[T, Any]:
        """Finds a model instance by its primary key."""
        pass
