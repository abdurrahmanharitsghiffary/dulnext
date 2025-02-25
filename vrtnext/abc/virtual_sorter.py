from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VirtualSorter(ABC):
    sorterable: List[str]

    def __init__(self, sorterable: List[str]):
        self.sorterable = sorterable

    @abstractmethod
    def sort_mapper(self, frappe_sorter: str) -> Dict[str, Any]:
        """Map frappe sort value like '`tabPost JSON Placeholder`.`dfquser_id` desc' into API or DATABASE sorter."""
        pass
