from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VirtualFilters(ABC):
    @abstractmethod
    def filters_mapper(self, filters: List[List[str]]) -> Dict[str, Any]:
        """Depends on the database type you should map the filters by yourself, for example we provide mapper for postgresql database, while using rest api we must define it by ourself because rest api always have different response structure"""
        pass
