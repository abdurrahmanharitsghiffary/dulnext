from typing import Any, Dict


class Filterable:
    @staticmethod
    def filters_mapper(filters: Dict[str, Any]):
        """Depends on the database type you should map the filters by yourself, for example we provide mapper for postgresql database, while using rest api we must define it by ourself because rest api always have different response structure"""
        pass
