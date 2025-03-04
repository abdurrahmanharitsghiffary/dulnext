from vrtnext.common.context.client_side_context import ClientSideContext
from vrtnext.common.mapper.rest_model_mapper import RestModelMapper
from vrtnext.entities.json_placeholder.post import PostEntity
from vrtnext.json_placeholder.doctype.post_json_placeholder.post_dao import (
    PostDAO,
)


class PostContext(ClientSideContext):
    def __init__(self):
        super().__init__(
            PostDAO(),
            RestModelMapper(
                convention="camelcase", name_column="id", model_class=PostEntity
            ),
        )
