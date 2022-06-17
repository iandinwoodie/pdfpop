"""Collection of tests for pdfpop's commands module."""
import pathlib

import pytest

import pdfpop.commands
import pdfpop.form_config


def test_config_command_form_path_not_found(tmp_path):
    """Test that an error is raised if the form path is not found."""
    with pytest.raises(FileNotFoundError):
        pdfpop.commands.config(tmp_path / "not_found.pdf")


def test_config_command_config_path_exists(tmp_path):
    """Test that an error is raised if the config path already exists."""
    form_path = tmp_path / "form.pdf"
    form_cfg_path = pdfpop.form_config.get_default_path(form_path)
    form_cfg_path.touch()
    try:
        with pytest.raises(FileNotFoundError):
            pdfpop.commands.config(form_path)
    finally:
        form_cfg_path.unlink()
