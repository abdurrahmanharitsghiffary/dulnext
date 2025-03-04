from vrtnext.abc.virtual_context import VirtualContext
from vrtnext.abc.virtual_dao import VirtualDAO
from vrtnext.abc.virtual_mapper import VirtualMapper
from vrtnext.common.filters.client_side_filters import ClientSideFilters
from vrtnext.common.paginator.client_side_paginator import ClientSidePaginator


class ClientSideContext(VirtualContext):
    def __init__(self, virtual_dao: VirtualDAO, virtual_mapper: VirtualMapper):
        super().__init__(
            virtual_dao,
            ClientSidePaginator(),
            ClientSideFilters(),
            virtual_mapper,
        )
