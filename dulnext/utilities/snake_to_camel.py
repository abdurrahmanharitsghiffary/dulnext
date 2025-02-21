import re


def snake_to_camel(s: str) -> str:
    if s.startswith("_"):
        return "_" + re.sub(r"_([a-zA-Z])", lambda m: m.group(1).upper(), s[1:])
    return re.sub(r"_([a-zA-Z])", lambda m: m.group(1).upper(), s)
