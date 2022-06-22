"""Collection of tests for pdfpop's CLI."""
import pathlib
import re

from click.testing import CliRunner
import pytest
from pytest_mock import mocker

import pdfpop.__main__


@pytest.fixture(scope="session")
def cli_runner():
    """Fixture that returns a helper function to run the pdfpop CLI."""
    runner = CliRunner()

    def cli_main(*cli_args, **cli_kwargs):
        """Run pdfpop CLI main with the given args."""
        return runner.invoke(pdfpop.__main__.main, cli_args, **cli_kwargs)

    return cli_main


@pytest.fixture(params=["-h", "--help"])
def help_cli_flag(request):
    """Pytest fixture return all help invocation options."""
    return request.param


def test_cli_help(cli_runner, help_cli_flag):
    """Test CLI invocation display help message with `help` flag."""
    result = cli_runner(help_cli_flag)
    assert result.exit_code == 0
    assert result.output.startswith("Usage: pdfpop")


@pytest.fixture(params=["-V", "--version"])
def version_cli_flag(request):
    """Pytest fixture return all version invocation options."""
    return request.param


def test_cli_version(cli_runner, version_cli_flag):
    """Test CLI invocation display version message with `version` flag."""
    result = cli_runner(version_cli_flag)
    assert result.exit_code == 0
    assert re.search(
        r"^pdfpop \d+\.\d+\.\d+ from .* \(Python \d+.\d+\)$", result.output
    )


def test_cli_no_args(cli_runner):
    """Test CLI invocation with passing any arguments."""
    result = cli_runner()
    assert result.exit_code == 0
    assert result.output.startswith("Usage: pdfpop")


def test_cli_no_args_invalid_command(cli_runner):
    """Test CLI invocation with an invalid command."""
    result = cli_runner("invalid")
    assert result.exit_code == 2
    assert result.output.startswith("Usage: pdfpop")
    assert "Error: No such command 'invalid'." in result.output


def test_cli_no_args_invalid_option(cli_runner):
    """Test CLI invocation with an invalid command."""
    result = cli_runner("--invalid")
    assert result.exit_code == 2
    assert result.output.startswith("Usage: pdfpop")
    assert "Error: No such option: --invalid\n" in result.output


def test_cli_config(mocker, cli_runner):
    """Test CLI invocation of the `config` command."""
    mock_command = mocker.patch("pdfpop.commands.config")

    form_path = pathlib.Path("tests/data/blank.pdf")
    result = cli_runner("config", str(form_path))

    assert result.exit_code == 0
    mock_command.assert_called_once_with(form_path=form_path)


def test_cli_config_form_path_not_found(mocker, cli_runner):
    """Test `config` command invocation with a form path that doesn't exist."""
    mock_command = mocker.patch("pdfpop.commands.config")

    form_path = pathlib.Path("tests/data/does-not-exist.pdf")
    result = cli_runner("config", str(form_path))

    assert result.exit_code == 2
    assert "Error: Invalid value for 'FORM':" in result.output
    mock_command.assert_not_called()


def test_cli_run(mocker, cli_runner):
    """Test CLI invocation of the `run` command."""
    mock_command = mocker.patch("pdfpop.commands.run")

    config_path = pathlib.Path("tests/data/pdfpop-blank.json")
    data_path = pathlib.Path("tests/data/empty.csv")
    result = cli_runner("run", str(config_path), str(data_path))

    assert result.exit_code == 0
    mock_command.assert_called_once_with(
        config_path=config_path, data_path=data_path
    )


def test_cli_run_config_path_not_found(mocker, cli_runner):
    """Test `run` command invocation with a config path that doesn't exist."""
    mock_command = mocker.patch("pdfpop.commands.run")

    config_path = pathlib.Path("tests/data/does-not-exist.json")
    data_path = pathlib.Path("tests/data/empty.csv")
    result = cli_runner("run", str(config_path), str(data_path))

    assert result.exit_code == 2
    assert "Error: Invalid value for 'CONFIG':" in result.output
    mock_command.assert_not_called()


def test_cli_run_data_path_not_found(mocker, cli_runner):
    """Test `run` command invocation with a data path that doesn't exist."""
    mock_command = mocker.patch("pdfpop.commands.run")

    config_path = pathlib.Path("tests/data/pdfpop-blank.json")
    data_path = pathlib.Path("tests/data/does-not-exist.csv")
    result = cli_runner("run", str(config_path), str(data_path))

    assert result.exit_code == 2
    assert "Error: Invalid value for 'DATA':" in result.output
    mock_command.assert_not_called()
