from frappe.exceptions import ValidationError


class NotFoundException(ValidationError):
    pass


class DependencyNotInjectedException(RuntimeError):
    pass
