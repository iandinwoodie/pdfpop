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
