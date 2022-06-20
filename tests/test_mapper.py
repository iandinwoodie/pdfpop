"""Collection of tests for pdfpop's mapper module."""
import pytest

import pdfpop.mapper


def test_map_fields_empty_args_returns_empty_dict():
    """Tests that empty args result in an empty dict."""
    assert pdfpop.mapper.map_fields({}, {}) == {}


def test_map_fields_ignore_null_mapped_keys():
    """Tests that fields mapped to None are ignored."""
    fields = {"a1": None, "b1": "return 456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, {})
    assert mapped_fields == {"b1": 456}


def test_map_fields_value_mapped_keys():
    """Tests that keys mapped to values are supported."""
    fields = {"a1": 123, "b1": "456", "c1": "'789'"}
    mapped_fields = pdfpop.mapper.map_fields(fields, {})
    assert mapped_fields == {"a1": 123, "b1": 456, "c1": "789"}


def test_map_fields_col_mapped_keys():
    """Tests that keys mapped to columns are supported."""
    fields = {"a1": "a2", "b1": "b2"}
    data = {"a2": 123, "b2": "456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_map_fields_code_mapped_keys():
    """Tests that keys mapped to code are supported."""
    fields = {"a1": "122+1", "b1": "'45' + '6'"}
    mapped_fields = pdfpop.mapper.map_fields(fields, {})
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_map_fields_rv_mapped_keys():
    """Tests that keys mapped to return values are supported."""
    fields = {"a1": "return 122+1", "b1": 'return "456"'}
    mapped_fields = pdfpop.mapper.map_fields(fields, {})
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_map_fields_mixed_mapping_types():
    """Tests that mixed mapping types across independent keys are supported."""
    fields = {"a1": "122+1", "b1": "b2", "c1": "return '789'"}
    data = {"b2": 456}
    mapped_fields = pdfpop.mapper.map_fields(fields, data)
    assert mapped_fields == {"a1": 123, "b1": 456, "c1": "789"}


def test_map_fields_data_access():
    """Tests that mappings have data access."""
    fields = {"a1": "data['a2']", "b1": "return data['b2']"}
    data = {"a2": 123, "b2": "456"}
    mapped_fields = pdfpop.mapper.map_fields(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_map_fields_data_access_error():
    """Tests that mappings have data access."""
    fields = {"a1": "data['a2']", "b1": "return data['b2']"}
    data = {"a2": 123}
    with pytest.raises(KeyError):
        pdfpop.mapper.map_fields(fields, data)
