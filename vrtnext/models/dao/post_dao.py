from typing import Any, Dict, TypeVar

import requests

from vrtnext.abc.virtual_dao import VirtualDAO
from vrtnext.entities.post import PostEntity
from vrtnext.typings.virtual_dao import VirtualActionResponse, VirtualCountResponse, VirtualFindResponse, VirtuaListResponse

Entity = TypeVar("Entity", bound=PostEntity)


class PostDAO(VirtualDAO):
    def get_item_count(self, filters: Any, pagination: Dict[str, Any]) -> VirtualCountResponse[Any]:
        """Get model instances counts."""

        response = requests.get("https://jsonplaceholder.typicode.com/posts")

        data = response.json()

        return VirtualCountResponse(actual_response=None, data=len(data))

    def find_all(self, filters: Any, pagination: Dict[str, Any]) -> VirtuaListResponse[PostEntity, Any]:
        """Finds all model instances matching the given filters."""

        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts",
        )

        data = response.json()

        return VirtuaListResponse(actual_response=None, data=data)

    def destroy(self, name: str) -> VirtualActionResponse[int, Any]:
        """Deletes the current model instance from the database or API."""
        requests.delete("https://jsonplaceholder.typicode.com/posts/" + str(name))

        return VirtualActionResponse(actual_response=None, affected=1)

    def update(self, name: str, new_data: Entity) -> VirtualActionResponse[Entity, Any]:
        """Updates the model instance in the database or API."""

        response = requests.patch("https://jsonplaceholder.typicode.com/posts/" + str(name), new_data)  # type: ignore[arg-type]

        data = response.json()

        return VirtualActionResponse(actual_response=None, affected=data)

    def insert(self, data: Entity) -> VirtualActionResponse[Entity, Any]:
        """Inserts the model instance in the database or API."""

        response = requests.post("https://jsonplaceholder.typicode.com/posts", data)  # type: ignore[arg-type]

        data = response.json()

        return VirtualActionResponse(actual_response=None, affected=data)

    def find_one(
        self,
        filters: Any,
    ) -> VirtualFindResponse[PostEntity, Any]:
        """Finds a single model instance matching the given filters."""

        response = requests.get("https://jsonplaceholder.typicode.com/posts")

        data = response.json()

        return VirtualFindResponse(data=data, actual_response=None)

    def find_one_by_pk(self, name: str) -> VirtualFindResponse[PostEntity, Any]:
        """Finds a model instance by its primary key."""
        response = requests.get("https://jsonplaceholder.typicode.com/posts/" + str(name))

        data = response.json()

        return VirtualFindResponse(data=data, actual_response=None)
