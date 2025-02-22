from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.context.rest_context import RestContext
from dulnext.models.dao.post_dao import PostDAO
from dulnext.models.filters.json_placeholder_api_filters_mapper import JSONPlaceholderAPIFiltersMapper
from dulnext.models.paginator.json_placeholder_api_pagination_mapper import JSONPlaceholderAPIPaginationMapper


class PostContext(RestContext):
    def __init__(self):
        super().__init__(
            RestMapper(convention="camelcase", name_column="id"),
            PostDAO(),
            JSONPlaceholderAPIPaginationMapper(),
            JSONPlaceholderAPIFiltersMapper(),
        )
