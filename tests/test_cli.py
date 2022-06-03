"""Collection of tests around pdfpop's CLI."""
from click.testing import CliRunner
import pytest

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
    assert result.output.startswith("Usage")


@pytest.fixture(params=["-V", "--version"])
def version_cli_flag(request):
    """Pytest fixture return all version invocation options."""
    return request.param


def test_cli_version(cli_runner, version_cli_flag):
    """Test CLI invocation display version message with `version` flag."""
    result = cli_runner(version_cli_flag)
    assert result.exit_code == 0
    assert result.output.startswith("pdfpop")
