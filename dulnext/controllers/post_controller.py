from dulnext.controllers.rest_controller import RestController
from dulnext.models.context.post_context import PostContext

POST_CONTEXT = PostContext()


class PostController(RestController):
    def db_insert(self, *args, **kwargs):
        return RestController.db_insert(self, POST_CONTEXT, *args, **kwargs)

    def load_from_db(self):
        return RestController.load_from_db(self, POST_CONTEXT)

    def db_update(self):
        return RestController.db_update(self, POST_CONTEXT)

    @staticmethod
    def get_list(args):
        return RestController.get_list(args, POST_CONTEXT)

    @staticmethod
    def get_count(args):
        return RestController.get_count(args, POST_CONTEXT)
