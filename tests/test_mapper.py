"""Collection of tests for pdfpop's mapper module."""
import pytest

import pdfpop.mapper


def test_mapper_map_fields_empty_args_returns_empty_dict():
    """Tests that empty args result in an empty dict."""
    assert pdfpop.mapper.map_fields({}, {}) == {}


def test_mapper_map_fields_null_value_ignoed():
    """Tests that fields mapped to None are ignored."""
    fields = {"a1": None, "b1": "return 456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, {})
    assert mapped_fields == {"b1": 456}


def test_mapper_map_fields_column_as_value():
    """Tests that column as value works."""
    fields = {"a1": "a2", "b1": "b2"}
    data = {"a2": 123, "b2": "456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_mapper_map_fields_function_as_value():
    """Tests that functions as values works."""
    fields = {"a1": "return 122+1", "b1": 'return "456"'}
    mapped_fields = pdfpop.mapper.map_fields(fields, {})
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_mapper_map_fields_mixed_type_values():
    """Tests that a mix of functions and columns as values works."""
    fields = {"a1": "return 122+1", "b1": "b2"}
    data = {"b2": "456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_mapper_map_fields_invalid_column_errors():
    """Tests that an invalid column results in a name error."""
    fields = {"a1": "a2"}
    with pytest.raises(NameError):
        mapped_fields = pdfpop.mapper.map_fields(fields, {})


def test_mapper_map_fields_function_data_access():
    """Tests that functions can access data."""
    fields = {"a1": "return data['a2']", "b1": "return data['b2']"}
    data = {"a2": 123, "b2": "456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}
