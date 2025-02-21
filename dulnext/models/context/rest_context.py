from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.context.virtual_context import VirtualContext
from dulnext.models.dao.virtual_dao import VirtualDAO
from dulnext.models.filters.filterable import Filterable
from dulnext.models.paginator.paginated import Paginated


class RestContext(VirtualContext):
    def __init__(
        self,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
        paginated: Paginated,
        filterable: Filterable,
    ):
        super().__init__(virtual_dao, paginated, filterable, rest_mapper)
