"""Collection of tests for pdfpop's form configuration files."""
import pathlib

import pytest

import pdfpop.form_config


def test_get_default_path():
    """Test that the expected default path is returned."""
    form_path = pathlib.Path("tests/files/blank.pdf")
    expected_path = pathlib.Path().cwd() / "pdfpop-blank.json"
    assert pdfpop.form_config.get_default_path(form_path) == expected_path
    assert (
        pdfpop.form_config.get_default_path(pathlib.Path(form_path.name))
        == expected_path
    )
    assert (
        pdfpop.form_config.get_default_path(form_path.resolve())
        == expected_path
    )


def test_form_config_exists():
    """Test that the form config exists."""
    form_cfg = pdfpop.form_config.FormConfig(
        pathlib.Path("tests/files/pdfpop-blank.json")
    )
    assert form_cfg.exists() == True


def test_form_config_exists_false():
    """Test that the form config does not exist."""
    form_cfg = pdfpop.form_config.FormConfig(
        pathlib.Path("tests/files/does-not-exist.json")
    )
    assert form_cfg.exists() == False


def test_interpret_empty_args_returns_empty_dict():
    """Tests that empty args result in an empty dict."""
    assert pdfpop.form_config.interpret({}, {}) == {}


def test_interpret_ignore_null_mapped_keys():
    """Tests that fields mapped to None are ignored."""
    fields = {"a1": None, "b1": "return 456"}
    mapped_fields = pdfpop.form_config.interpret(fields, {})
    assert mapped_fields == {"b1": 456}


def test_interpret_value_mapped_keys():
    """Tests that keys mapped to values are supported."""
    fields = {"a1": 123, "b1": "456", "c1": "'789'"}
    mapped_fields = pdfpop.form_config.interpret(fields, {})
    assert mapped_fields == {"a1": 123, "b1": 456, "c1": "789"}


def test_interpret_col_mapped_keys():
    """Tests that keys mapped to columns are supported."""
    fields = {"a1": "a2", "b1": "b2"}
    data = {"a2": 123, "b2": "456"}
    mapped_fields = pdfpop.form_config.interpret(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_interpret_code_mapped_keys():
    """Tests that keys mapped to code are supported."""
    fields = {"a1": "122+1", "b1": "'45' + '6'"}
    mapped_fields = pdfpop.form_config.interpret(fields, {})
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_interpret_rv_mapped_keys():
    """Tests that keys mapped to return values are supported."""
    fields = {"a1": "return 122+1", "b1": 'return "456"'}
    mapped_fields = pdfpop.form_config.interpret(fields, {})
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_interpret_mixed_mapping_types():
    """Tests that mixed mapping types across independent keys are supported."""
    fields = {"a1": "122+1", "b1": "b2", "c1": "return '789'"}
    data = {"b2": 456}
    mapped_fields = pdfpop.form_config.interpret(fields, data)
    assert mapped_fields == {"a1": 123, "b1": 456, "c1": "789"}


def test_interpret_data_access():
    """Tests that mappings have data access."""
    fields = {"a1": "data['a2']", "b1": "return data['b2']"}
    data = {"a2": 123, "b2": "456"}
    mapped_fields = pdfpop.form_config.interpret(fields, data)
    assert mapped_fields == {"a1": 123, "b1": "456"}


def test_interpret_data_access_error():
    """Tests that mappings have data access."""
    fields = {"a1": "data['a2']", "b1": "return data['b2']"}
    data = {"a2": 123}
    with pytest.raises(KeyError):
        pdfpop.form_config.interpret(fields, data)
