import re


def camel_to_snake(s: str) -> str:
    if s.startswith("_"):
        return "_" + re.sub(r"([A-Z])", r"_\1", s[1:]).lower()
    return re.sub(r"([A-Z])", r"_\1", s).lower()
