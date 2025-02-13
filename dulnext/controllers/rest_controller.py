from .virtual_controller import VirtualController


class RestMapper:
    def map_rest_to_doc(self):
        pass

    def map_doc_to_rest(self):
        pass

    def map_form_to_creatable(self):
        pass

    def map_form_to_updateble(self):
        pass


class RestController(RestMapper, VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    pass
