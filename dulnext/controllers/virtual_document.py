from frappe.model.document import Document

from dulnext.utilities.virtual import validate_doctype_without_select


class VirtualDocument(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        validate_doctype_without_select(self)
