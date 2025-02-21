from typing import Any, Dict, List

from dulnext.models.filters.filterable import Filterable


class JSONPlaceholderAPIFiltersMapper(Filterable):
    def filters_mapper(self, filters: List[List[str]]) -> Dict[str, Any]:
        return {}
