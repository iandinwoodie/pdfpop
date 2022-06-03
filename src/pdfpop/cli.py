"""CLI module for pdfpop."""
import pathlib
import sys

import click

from pdfpop import __version__
from pdfpop.main import pdfpop


def version_msg():
    """Return the pdfpop version message string template."""
    python_version = ".".join(map(str, sys.version_info[0:2]))
    location = pathlib.Path(__file__).resolve().parents[1]
    return f"%(prog)s %(version)s from {location} (Python {python_version})"


@click.command(name="pdfpop", context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.argument("pdf", type=click.Path(exists=True))
@click.argument("excel", type=click.Path(exists=True))
@click.option("-o", "--output", default="populated.pdf", help="Output file path.")
def main(pdf, excel, output):
    """Populate a PDF file with data from Excel."""
    pdfpop(input_pdf_path=pdf, input_excel_path=excel, output_pdf_path=output)


if __name__ == "__main__":
    main()
