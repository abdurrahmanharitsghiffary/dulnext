from dulnext.entities.post import PostEntity
from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.context.client_side_context import ClientSideContext
from dulnext.models.dao.post_dao import PostDAO


class PostContext(ClientSideContext):
    def __init__(self):
        super().__init__(
            PostDAO(),
            RestMapper(convention="camelcase", name_column="id", doc_model=PostEntity),
        )
