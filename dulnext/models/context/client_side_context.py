from dulnext.mapper.virtual_mapper import VirtualMapper
from dulnext.models.dao.virtual_dao import VirtualDAO
from dulnext.models.filters.client_side_filters import ClientSideFilters
from dulnext.models.paginator.client_side_paginator import ClientSidePaginator

from .virtual_context import VirtualContext


class ClientSideContext(VirtualContext):
    def __init__(self, virtual_dao: VirtualDAO, virtual_mapper: VirtualMapper):
        super().__init__(virtual_dao, ClientSidePaginator(), ClientSideFilters(), virtual_mapper)
