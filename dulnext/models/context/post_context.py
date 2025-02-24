from dulnext.entities.post import PostEntity
from dulnext.mapper.rest_model_mapper import RestModelMapper
from dulnext.models.context.client_side_context import ClientSideContext
from dulnext.models.dao.post_dao import PostDAO


class PostContext(ClientSideContext):
    def __init__(self):
        super().__init__(
            PostDAO(),
            RestModelMapper(convention="camelcase", name_column="id", model_class=PostEntity),
        )
