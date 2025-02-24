import re


def camel_to_snake(s: str) -> str:
    # Preserve leading underscores
    prefix = ""
    while s.startswith("_"):
        prefix += "_"
        s = s[1:]
    # First, insert underscores before capital letters that start a word (followed by lowercase letters)
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    # Then, insert underscores between a lowercase/digit and an uppercase letter (for transitions like "lT")
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return prefix + s2.lower()
