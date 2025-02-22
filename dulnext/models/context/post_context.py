from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.context.rest_context import RestContext
from dulnext.models.dao.post_dao import PostDAO
from dulnext.models.filters.client_side_filters import ClientSideFilters
from dulnext.models.paginator.client_side_paginator import ClientSidePaginator


class PostContext(RestContext):
    def __init__(self):
        super().__init__(
            RestMapper(convention="camelcase", name_column="id"),
            PostDAO(),
            ClientSidePaginator(),
            ClientSideFilters(),
        )
