from abc import ABC, abstractmethod
from typing import Any, Dict

from vrtnext.typings.pagination_options import PaginationOptions


class VirtualPaginator(ABC):
    @abstractmethod
    def pagination_mapper(self, options: PaginationOptions) -> Dict[str, Any]:
        """Mapper method for pagination passed by frappe."""
        pass
