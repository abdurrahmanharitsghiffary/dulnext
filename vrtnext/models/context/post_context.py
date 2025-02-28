from vrtnext.entities.post import PostEntity
from vrtnext.mapper.rest_model_mapper import RestModelMapper
from vrtnext.models.context.client_side_context import ClientSideContext
from vrtnext.models.dao.post_dao import PostDAO


class PostContext(ClientSideContext):
    def __init__(self):
        super().__init__(
            PostDAO(),
            RestModelMapper(
                convention="camelcase", name_column="id", model_class=PostEntity
            ),
        )
