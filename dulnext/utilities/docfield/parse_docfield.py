from typing import Optional


class ParseDFReturn:
    fieldname: str
    docfield_type: str
    special_type: str


def parse_docfield(df: str) -> Optional[ParseDFReturn]:
    # Create an instance of the ParseDFReturn class
    result = ParseDFReturn()

    # Find the index of "spq" and "df" in the string
    index_spq = df.find("spq")
    index_dfq = df.find("dfq")

    if index_spq != -1 and index_dfq != -1:
        # Extract special_type and docfield_type using the indices
        result.special_type = df[0:index_spq]
        result.docfield_type = df[index_spq + 3 : index_dfq]
        result.fieldname = df[index_dfq + 3 :]

        result.fieldname = ".".join(result.fieldname.split("dot"))
        return result
    else:
        print("Error: 'spq' and/or 'dfq' not found in the string")
        return None
