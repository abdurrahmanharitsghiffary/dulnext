from typing import List, Optional

from pydantic import BaseModel


class BaseVirtualResponse[T, AR](BaseModel):
    # List data that will be mapped to doctype
    data: T

    # The actual response, may be a response from API or Database
    actual_response: AR


class BaseVirtualActionResponse[T, AR](BaseModel):
    # Might be affected rows number
    affected: T

    # The actual response, may be a response from API or Database
    actual_response: AR


class VirtuaListResponse[T, AR](BaseVirtualResponse[List[T], AR]):
    pass


class VirtualFindResponse[T, AR](BaseVirtualResponse[Optional[T], AR]):
    pass


# Of course it will return int
class VirtualCountResponse[AR](BaseVirtualResponse[int, AR]):
    pass


class VirtualActionResponse[T, AR](BaseVirtualActionResponse[T, AR]):
    pass
