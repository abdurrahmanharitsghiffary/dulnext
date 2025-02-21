from typing import Any, Dict, List


class Sorter:
    # Field that can be sortered
    sorterable: List[str]

    def sort_mapper(self, frappe_sorter: str) -> Dict[str, Any]:
        """Map frappe sort value like '`tabPost JSON Placeholder`.`dfquser_id` desc' into API or DATABASE sorter."""
        raise NotImplementedError("Method not implemented.")
