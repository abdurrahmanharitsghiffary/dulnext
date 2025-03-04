from vrtnext.abc.virtual_context import VirtualContext
from vrtnext.abc.virtual_dao import VirtualDAO
from vrtnext.abc.virtual_filters import VirtualFilters
from vrtnext.abc.virtual_paginator import VirtualPaginator
from vrtnext.common.mapper.rest_mapper import RestMapper


class RestContext(VirtualContext):
    def __init__(
        self,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
        paginated: VirtualPaginator,
        filterable: VirtualFilters,
    ):
        super().__init__(virtual_dao, paginated, filterable, rest_mapper)
