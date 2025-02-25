from abc import ABC
from typing import Optional

from vrtnext.abc.virtual_dao import VirtualDAO
from vrtnext.abc.virtual_filters import VirtualFilters
from vrtnext.abc.virtual_mapper import VirtualMapper
from vrtnext.abc.virtual_paginator import VirtualPaginator
from vrtnext.exceptions import MissingDependencyError


class VirtualContext(ABC):
    _virtual_dao: Optional[VirtualDAO] = None
    _filterable: Optional[VirtualFilters] = None
    _paginated: Optional[VirtualPaginator] = None
    _virtual_mapper: Optional[VirtualMapper] = None

    def __init__(
        self,
        virtual_dao: VirtualDAO,
        paginated: VirtualPaginator,
        filterable: VirtualFilters,
        virtual_mapper: VirtualMapper,
    ):
        self._filterable = filterable
        self._paginated = paginated
        self._virtual_dao = virtual_dao
        self._virtual_mapper = virtual_mapper

    def get_filter_mapper(self) -> VirtualFilters:
        if not self._filterable:
            raise MissingDependencyError("Failed to get the VirtualFilters")

        return self._filterable

    def get_pagination_mapper(self) -> VirtualPaginator:
        if not self._paginated:
            raise MissingDependencyError("Failed to get the Paginated")

        return self._paginated

    def get_dao(self) -> VirtualDAO:
        if not self._virtual_dao:
            raise MissingDependencyError("Failed to get the VirtualDAO")

        return self._virtual_dao

    def get_mapper(self):
        if not self._virtual_mapper:
            raise MissingDependencyError("Failed to get the VirtualMapper")

        return self._virtual_mapper
