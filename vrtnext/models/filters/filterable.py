from typing import Any, Dict, List


class Filterable:
    def filters_mapper(self, filters: List[List[str]]) -> Dict[str, Any]:
        """Depends on the database type you should map the filters by yourself, for example we provide mapper for postgresql database, while using rest api we must define it by ourself because rest api always have different response structure"""

        raise NotImplementedError("Method not implemented.")

    # def equals_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")

    # def not_equals_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")

    # def likes_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")

    # def not_likes_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")

    # def not_in_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")

    # def in_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")

    # def ls_map(self, filters: List[List[str]]) -> Dict[str, Any]:
    #     """Should return dict that will be used in requests"""
    #     raise NotImplementedError("Method not implemented.")
