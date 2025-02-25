from typing import Any, Dict

from vrtnext.typings.pagination_options import PaginationOptions


class Paginated:
    def pagination_mapper(self, options: PaginationOptions) -> Dict[str, Any]:
        """Mapper method for pagination passed by frappe us"""
        raise NotImplementedError("Method not implemented.")
