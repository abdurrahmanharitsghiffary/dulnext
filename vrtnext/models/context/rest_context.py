from vrtnext.mapper.rest_mapper import RestMapper
from vrtnext.models.context.virtual_context import VirtualContext
from vrtnext.models.dao.virtual_dao import VirtualDAO
from vrtnext.models.filters.filterable import Filterable
from vrtnext.models.paginator.paginated import Paginated


class RestContext(VirtualContext):
    def __init__(
        self,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
        paginated: Paginated,
        filterable: Filterable,
    ):
        super().__init__(virtual_dao, paginated, filterable, rest_mapper)
