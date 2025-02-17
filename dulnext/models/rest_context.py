from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.filterable import Filterable
from dulnext.models.paginated import Paginated
from dulnext.models.virtual_context import VirtualContext
from dulnext.models.virtual_dao import VirtualDAO


class RestContext(VirtualContext):
    def __init__(
        self,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
        paginated: Paginated,
        filterable: Filterable,
    ):
        super().__init__(virtual_dao, paginated, filterable, rest_mapper)
