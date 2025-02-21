from typing import Any, Dict

from dulnext.models.paginator.paginated import Paginated
from dulnext.typings.pagination_options import PaginationOptions


class JSONPlaceholderAPIPaginationMapper(Paginated):
    def pagination_mapper(self, options: PaginationOptions) -> Dict[str, Any]:
        return {}
