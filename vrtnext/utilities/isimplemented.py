from typing import Callable


def isimplemented[
    ReturnType
](callable: Callable[[], ReturnType]) -> ReturnType | bool:
    """Determine if a method is implemented or not, if not it will return False."""
    try:
        return callable()
    except NotImplementedError:
        return False
