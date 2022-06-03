"""Collection of tests around pdfpop's CLI."""
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


@pytest.fixture(params=["-o", "--output"])
def output_flag(request):
    """Pytest fixture return all output invocation options."""
    return request.param


def test_cli_output(mocker, cli_runner, output_flag):
    """Test CLI invocation with `output` flag."""
    mock_pdfpop = mocker.patch("pdfpop.cli.pdfpop")

    pdf = "tests/files/fake-form.pdf"
    excel = "tests/files/fake-data.xlsx"
    output = "tests/fake-output.pdf"
    result = cli_runner(pdf, excel, output_flag, output)

    assert result.exit_code == 0
    mock_pdfpop.assert_called_once_with(
        input_pdf_path=pdf, input_excel_path=excel, output_pdf_path=output
    )


def test_cli_no_options(mocker, cli_runner):
    mock_pdfpop = mocker.patch("pdfpop.cli.pdfpop")

    pdf = "tests/files/fake-form.pdf"
    excel = "tests/files/fake-data.xlsx"
    result = cli_runner(pdf, excel)

    output = "populated.pdf"
    assert result.exit_code == 0
    mock_pdfpop.assert_called_once_with(
        input_pdf_path=pdf, input_excel_path=excel, output_pdf_path=output
    )
