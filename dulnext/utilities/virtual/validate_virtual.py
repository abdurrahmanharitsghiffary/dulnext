# A controller can only inherit directly from Document
# multiple inheritance with Document is not supported.
# To work around this, we use a custom function and override the method directly in the controller API.

from frappe.model import optional_fields
from frappe.model.document import Document


def validate_doctype_without_select(self: Document):
    """Utility function for use in the _validate method of controllers."""
    self._validate_mandatory()
    self._validate_data_fields()
    # self._validate_selects()
    self._validate_non_negative()
    self._validate_length()
    self._fix_rating_value()
    self._validate_code_fields()
    self._sync_autoname_field()
    self._extract_images_from_editor()
    self._sanitize_content()
    self._save_passwords()
    self.validate_workflow()
    for d in self.get_all_children():
        d._validate_data_fields()
        # d._validate_selects()
        d._validate_non_negative()
        d._validate_length()
        d._fix_rating_value()
        d._validate_code_fields()
        d._sync_autoname_field()
        d._extract_images_from_editor()
        d._sanitize_content()
        d._save_passwords()
    if self.is_new():
        # don't set fields like _assign, _comments for new doc
        for fieldname in optional_fields:
            self.set(fieldname, None)
    else:
        self.validate_set_only_once()
