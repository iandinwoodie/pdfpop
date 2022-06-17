"""Collection of tests around pdfpop's CLI."""
import re

from click.testing import CliRunner
import pytest
from pytest_mock import mocker

from pdfpop.__main__ import main


@pytest.fixture(scope="session")
def cli_runner():
    """Fixture that returns a helper function to run the pdfpop CLI."""
    runner = CliRunner()

    def cli_main(*cli_args, **cli_kwargs):
        """Run pdfpop CLI main with the given args."""
        return runner.invoke(main, cli_args, **cli_kwargs)

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


def test_cli_no_args(mocker, cli_runner):
    """Test CLI invocation with passing any arguments."""
    result = cli_runner()
    assert result.exit_code == 0
    assert result.output.startswith("Usage: pdfpop")


def test_cli_config(cli_runner):
    """Test CLI invocation of the `config` command."""
    form = "tests/files/blank.pdf"
    result = cli_runner("config", form)
    assert result.exit_code == 0
    assert result.output.startswith("CONFIG COMMAND")


def test_cli_run(cli_runner):
    """Test CLI invocation of the `run` command."""
    config = "tests/files/pdfpop-blank.json"
    data = "tests/files/empty.csv"
    result = cli_runner("run", config, data)
    assert result.exit_code == 0
    assert result.output.startswith("RUN COMMAND")
