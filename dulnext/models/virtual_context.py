from typing import Optional

from dulnext.exceptions import MissingDependencyError
from dulnext.mapper.virtual_mapper import VirtualMapper
from dulnext.models.filterable import Filterable
from dulnext.models.paginated import Paginated
from dulnext.models.virtual_dao import VirtualDAO


class VirtualContext:
    _virtual_dao: Optional[VirtualDAO] = None
    _filterable: Optional[Filterable] = None
    _paginated: Optional[Paginated] = None
    _virtual_mapper: Optional[VirtualMapper] = None

    def __init__(
        self,
        virtual_dao: VirtualDAO,
        paginated: Paginated,
        filterable: Filterable,
        virtual_mapper: VirtualMapper,
    ):
        self._filterable = filterable
        self._paginated = paginated
        self._virtual_dao = virtual_dao
        self._virtual_mapper = virtual_mapper

    def get_filter_mapper(self) -> Filterable:
        if not self._filterable:
            raise MissingDependencyError("Failed to get the Filterable")

        return self._filterable

    def get_pagination_mapper(self) -> Paginated:
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
