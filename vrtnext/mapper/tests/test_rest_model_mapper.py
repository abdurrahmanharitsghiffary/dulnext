from dataclasses import dataclass

import pytest

from ..rest_model_mapper import RestModelMapper


@dataclass
class SampleEntity:
    dfqdtatitle: str
    dfqdtauserdotfull_namedotfirst_name: str
    dfqdtauserdotfull_namedotlast_name: str
    dfqdtauserdotid: str
    dfqdtecreated_at: str
    dfqdtaspqidxuserdotlegal_names: str


@pytest.fixture
def camelcase_mapper():
    return RestModelMapper(
        model_class=SampleEntity, name_column="id", convention="camelcase"
    )


@pytest.fixture
def lowercase_mapper():
    return RestModelMapper(
        model_class=SampleEntity, name_column="id", convention="lowercase"
    )


def test_map_doc_to_item_camelcase(camelcase_mapper: RestModelMapper) -> None:
    doc = {
        "dfqdtatitle": "Loler Title",
        "dfqdtauserdotfull_namedotfirst_name": "Firstname",
        "dfqdtauserdotfull_namedotlast_name": "Lastname",
        "dfqdtauserdotid": "some-uuid-v4",
        "dfqdtecreated_at": "2024-03-25",
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    expected_item = {
        "title": "Loler Title",
        "user": {
            "fullName": {
                "firstName": "Firstname",
                "lastName": "Lastname",
            },
            "id": "some-uuid-v4",
        },
        "createdAt": "2024-03-25",
    }
    result = camelcase_mapper.map_doc_to_item(doc, ignore_optional=True)
    assert result == expected_item


def test_map_doc_to_item_camelcase_no_ignore_optional(
    camelcase_mapper: RestModelMapper,
) -> None:
    doc = {
        "dfqdtatitle": "Loler Title",
        "dfqdtauserdotfull_namedotfirst_name": "Firstname",
        "dfqdtauserdotfull_namedotlast_name": "Lastname",
        "dfqdtauserdotid": "some-uuid-v4",
        "dfqdtecreated_at": "2024-03-25",
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    expected_item = {
        "title": "Loler Title",
        "user": {
            "fullName": {
                "firstName": "Firstname",
                "lastName": "Lastname",
            },
            "id": "some-uuid-v4",
            "legalNames": None,
        },
        "createdAt": "2024-03-25",
    }
    result = camelcase_mapper.map_doc_to_item(doc, ignore_optional=False)
    assert result == expected_item


def test_map_item_to_doc_camelcase(camelcase_mapper: RestModelMapper) -> None:
    item = {
        "title": "Lolerzzz",
        "user": {
            "username": None,
            "jamalodon": None,
            "fullName": {"firstName": "Jamal", "lastName": "Boolean"},
            "id": "loleresss-uuidv4",
        },
        "createdAt": "2025-03-14",
    }

    doc = {
        "dfqdtatitle": None,
        "dfqdtauserdotfull_namedotfirst_name": None,
        "dfqdtauserdotfull_namedotlast_name": None,
        "dfqdtauserdotid": None,
        "dfqdtecreated_at": None,
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    # Expected document after mapping values from the item.
    expected_doc = {
        "dfqdtatitle": "Lolerzzz",
        "dfqdtauserdotfull_namedotfirst_name": "Jamal",
        "dfqdtauserdotfull_namedotlast_name": "Boolean",
        "dfqdtauserdotid": "loleresss-uuidv4",
        "dfqdtecreated_at": "2025-03-14",
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    camelcase_mapper.map_item_to_doc(item, doc)
    assert doc == expected_doc


def test_map_doc_to_item_lowercase(lowercase_mapper: RestModelMapper) -> None:
    doc = {
        "dfqdtatitle": "Loler Title",
        "dfqdtauserdotfull_namedotfirst_name": "Firstname",
        "dfqdtauserdotfull_namedotlast_name": "Lastname",
        "dfqdtauserdotid": "some-uuid-v4",
        "dfqdtecreated_at": "2024-03-25",
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    expected_item = {
        "title": "Loler Title",
        "user": {
            "full_name": {
                "first_name": "Firstname",
                "last_name": "Lastname",
            },
            "id": "some-uuid-v4",
        },
        "created_at": "2024-03-25",
    }
    result = lowercase_mapper.map_doc_to_item(doc, ignore_optional=True)
    assert result == expected_item


def test_map_doc_to_item_lowercase_no_ignore_optional(
    lowercase_mapper: RestModelMapper,
) -> None:
    doc = {
        "dfqdtatitle": "Loler Title",
        "dfqdtauserdotfull_namedotfirst_name": "Firstname",
        "dfqdtauserdotfull_namedotlast_name": "Lastname",
        "dfqdtauserdotid": "some-uuid-v4",
        "dfqdtecreated_at": "2024-03-25",
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    expected_item = {
        "title": "Loler Title",
        "user": {
            "full_name": {
                "first_name": "Firstname",
                "last_name": "Lastname",
            },
            "id": "some-uuid-v4",
            "legal_names": None,
        },
        "created_at": "2024-03-25",
    }
    result = lowercase_mapper.map_doc_to_item(doc, ignore_optional=False)
    assert result == expected_item


def test_map_item_to_doc_lowercase(lowercase_mapper: RestModelMapper) -> None:
    item = {
        "title": "Lolerzzz",
        "user": {
            "username": None,
            "jamalodon": None,
            "full_name": {"first_name": "Jamal", "last_name": "Boolean"},
            "id": "loleresss-uuidv4",
        },
        "created_at": "2025-03-14",
    }

    doc = {
        "dfqdtatitle": None,
        "dfqdtauserdotfull_namedotfirst_name": None,
        "dfqdtauserdotfull_namedotlast_name": None,
        "dfqdtauserdotid": None,
        "dfqdtecreated_at": None,
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    # Expected document after mapping values from the item.
    expected_doc = {
        "dfqdtatitle": "Lolerzzz",
        "dfqdtauserdotfull_namedotfirst_name": "Jamal",
        "dfqdtauserdotfull_namedotlast_name": "Boolean",
        "dfqdtauserdotid": "loleresss-uuidv4",
        "dfqdtecreated_at": "2025-03-14",
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    lowercase_mapper.map_item_to_doc(item, doc)
    assert doc == expected_doc


def test_map_item_to_doc_spqidx(lowercase_mapper: RestModelMapper) -> None:
    item = {
        "title": "Lolerzzz",
        "user": {
            "username": None,
            "jamalodon": None,
            "full_name": {
                "first_name": "Jamal",
                "last_name": "Boolean",
            },
            "legal_names": [
                "Jamal Boolean",
                "Jimmy Boolean",
                "Joko Widada",
                "Agus Syedih",
            ],
            "id": "loleresss-uuidv4",
        },
        "created_at": "2025-03-14",
    }

    doc = {
        "dfqdtatitle": None,
        "dfqdtauserdotfull_namedotfirst_name": None,
        "dfqdtauserdotfull_namedotlast_name": None,
        "dfqdtauserdotid": None,
        "dfqdtecreated_at": None,
        "dfqdtaspqidxuserdotlegal_names": None,
    }
    # Expected document after mapping values from the item.
    expected_doc = {
        "dfqdtatitle": "Lolerzzz",
        "dfqdtauserdotfull_namedotfirst_name": "Jamal",
        "dfqdtauserdotfull_namedotlast_name": "Boolean",
        "dfqdtauserdotid": "loleresss-uuidv4",
        "dfqdtecreated_at": "2025-03-14",
        "dfqdtaspqidxuserdotlegal_names": "Jamal Boolean, Jimmy Boolean, Joko Widada, Agus Syedih",
    }

    lowercase_mapper.map_item_to_doc(item, doc)
    assert doc == expected_doc


def test_map_doc_to_item_spqidx(lowercase_mapper: RestModelMapper) -> None:
    doc = {
        "dfqdtatitle": "Loler Title",
        "dfqdtauserdotfull_namedotfirst_name": "Firstname",
        "dfqdtauserdotfull_namedotlast_name": "Lastname",
        "dfqdtauserdotid": "some-uuid-v4",
        "dfqdtecreated_at": "2024-03-25",
        "dfqdtaspqidxuserdotlegal_names": "Jamal Boolean, Jimmy Boolean, Joko Widada, Agus Syedih",
    }
    expected_item = {
        "title": "Loler Title",
        "user": {
            "full_name": {
                "first_name": "Firstname",
                "last_name": "Lastname",
            },
            "id": "some-uuid-v4",
            "legal_names": [
                "Jamal Boolean",
                "Jimmy Boolean",
                "Joko Widada",
                "Agus Syedih",
            ],
        },
        "created_at": "2024-03-25",
    }
    result = lowercase_mapper.map_doc_to_item(doc, ignore_optional=True)
    assert result == expected_item
