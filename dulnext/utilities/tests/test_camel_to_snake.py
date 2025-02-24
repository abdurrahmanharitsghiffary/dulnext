from dulnext.utilities import camel_to_snake


def test_camel_to_snake_normal():
    # Typical camelCase string starting with a lowercase letter.
    input_str = "camelToSnake"
    expected = "camel_to_snake"
    assert camel_to_snake(input_str) == expected


def test_camel_to_snake_leading_capital():
    # String starting with an uppercase letter.
    input_str = "CamelToSnake"
    # Note: As implemented, this will prepend an underscore.
    expected = "camel_to_snake"
    assert camel_to_snake(input_str) == expected


def test_camel_to_snake_with_leading_underscore_lower():
    # String that already starts with an underscore and then a lowercase letter.
    input_str = "_camelToSnake"
    expected = "_camel_to_snake"
    assert camel_to_snake(input_str) == expected


def test_camel_to_snake_with_leading_underscore_upper():
    # String starting with an underscore followed by an uppercase letter.
    input_str = "_CamelToSnake"
    # The function preserves the initial underscore and then applies conversion,
    # resulting in two leading underscores.
    expected = "_camel_to_snake"
    assert camel_to_snake(input_str) == expected


def test_already_snake_case():
    # Input is already in snake_case.
    input_str = "snake_case"
    expected = "snake_case"
    assert camel_to_snake(input_str) == expected


def test_empty_string():
    # The empty string should return an empty string.
    input_str = ""
    expected = ""
    assert camel_to_snake(input_str) == expected


def test_multiple_capitals():
    # Test a string with consecutive uppercase letters.
    input_str = "HTTPRequest"
    input_str2 = "HTTPSRequest"
    # Each uppercase letter is prefixed by an underscore.
    expected = "http_request"
    expected2 = "https_request"
    assert camel_to_snake(input_str) == expected
    assert camel_to_snake(input_str2) == expected2
