from vrtnext.controllers.client_side_controller import ClientSideController
from vrtnext.models.context.post_context import PostContext

POST_CONTEXT = PostContext()


class PostController(ClientSideController):
    def db_insert(self, *args, **kwargs):
        return ClientSideController.db_insert(
            self, POST_CONTEXT, *args, **kwargs
        )

    def load_from_db(self):
        return ClientSideController.load_from_db(self, POST_CONTEXT)

    def db_update(self):
        print(f"First Self: {self}")
        return ClientSideController.db_update(self, POST_CONTEXT)

    @staticmethod
    def get_list(args):
        return ClientSideController.get_list(args, POST_CONTEXT)

    @staticmethod
    def get_count(args):
        return ClientSideController.get_count(args, POST_CONTEXT)
