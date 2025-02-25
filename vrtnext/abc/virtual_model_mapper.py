from abc import ABC
from typing import Dict, Literal, Optional

from .virtual_mapper import VirtualMapper


class VirtualModelMapper(VirtualMapper, ABC):
    """Extension class of the VirtualMapper"""

    model_class: type
    link_model_classes: Optional[Dict[str, type]]

    def __init__(
        self,
        model_class: type,
        link_model_classes: Optional[Dict[str, type]] = None,
        convention: Literal["camelcase", "snakecase"] = "snakecase",
        name_column: str = "id",
    ):
        self.model_class = model_class
        self.link_model_classes = link_model_classes
        super().__init__(convention, name_column)
