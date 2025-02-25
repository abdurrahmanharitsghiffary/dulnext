from vrtnext.models.docfield_meta import DocfieldMeta


def parse_docfield(df: str) -> DocfieldMeta:
    result = DocfieldMeta(docfield_type=None, fieldname=None, is_can_mapped=False, special_type=None)

    is_can_mapped = df.startswith("dfq")

    if not is_can_mapped:
        return result

    # Find the index of "spq" and "dfq" in the string
    index_spq = df.find("spq")
    index_dfq = df.find("dfq")

    # Extract special_type and docfield_type using the indices
    if index_spq != -1:
        result.special_type = df[index_spq + 3 : index_spq + 6]

    result.docfield_type = df[index_dfq + 3 : index_dfq + 6]

    field_index = 6

    if index_spq == -1:
        field_index = field_index + 1

    result.fieldname = df[index_spq + field_index :]

    result.is_can_mapped = True
    return result


# if __name__ == "__main__":
#     result = parse_docfield("dfqtlespqidxlolerdotsumpah")
#     result2 = parse_docfield("dfqdtalolerdotsumpah")
#     result3 = parse_docfield("dfqlnklolersumpah")
#     result4 = parse_docfield("dfqintspqidxlolerdotsumpah")
#     result5 = parse_docfield("dfqdtaspqidxlolerdotsumpah")
#     result6 = parse_docfield("dfqdta")

#     print(f"{result}")
#     print(f"{result2}")
#     print(f"{result3}")
#     print(f"{result4}")
#     print(f"{result5}")
#     print(f"{result6}")
