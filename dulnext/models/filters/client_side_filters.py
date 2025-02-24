from typing import Any, Dict, List

from .filterable import Filterable


class ClientSideFilters(Filterable):
    """
    Best suited for REST API that does not implemented all of frappe filters. This filters will fetch all data from find_all method in your VirtualDAO implementation.
    if the REST API already have filters implementation please map them by yourself instead. this Filters cannot be used by DatabaseContext. please use Postgresql or MariaDB Filters instead.
    This Filters must be used along ClientSidePaginator and RestContext.
    """

    def filters_mapper(self, filters: List[List[str]]) -> Dict[str, Any]:
        return {"is_client_side_filters": True, "filters": filters}
