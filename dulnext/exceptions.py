from typing import Optional


class CommonError(Exception):
    name: str = "CommonError"
    message: Optional[str] = None
    code: Optional[str] = None

    def __init__(self, message: Optional[str], code: Optional[str], *args):
        super().__init__(*args)
        self.message = message
        self.code = code


class MissingDependencyError(CommonError):
    def __init__(self, message, *args):
        super().__init__(message, "MISSDEPS", *args)
