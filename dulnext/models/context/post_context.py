from dulnext.mapper.json_placeholder_api_filters_mapper import JSONPlaceholderAPIFiltersMapper
from dulnext.mapper.json_placeholder_api_pagination_mapper import JSONPlaceholderAPIPaginationMapper
from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.context.rest_context import RestContext
from dulnext.models.dao.post_dao import PostDAO


class PostContext(RestContext):
    def __init__(self):
        super().__init__(
            RestMapper(convention="camelcase", name_column="id"),
            PostDAO(),
            JSONPlaceholderAPIPaginationMapper(),
            JSONPlaceholderAPIFiltersMapper(),
        )
