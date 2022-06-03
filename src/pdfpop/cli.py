"""CLI module for pdfpop."""
import sys
import pathlib
import argparse

from pdfpop import __version__
from pdfpop.main import pdfpop


def main():
    """Main pdfpop function."""
    args = parse_cli()
    pdfpop(args.pdf, args.excel, args.out)


def parse_cli():
    """Load command line arguments."""
    parser = argparse.ArgumentParser(description="Populate PDF from Excel.")
    parser.add_argument("--version", action="version", version=version_msg())
    parser.add_argument("excel", help="Excel file to use as data source")
    parser.add_argument("pdf", help="PDF to be populated")
    parser.add_argument(
        "-o",
        "--out",
        help="Write output to file",
        default="populated.pdf",
        metavar="POPULATED",
    )
    return parser.parse_args()


def version_msg():
    """Return the pdfpop version, location, and Python powering it."""
    python_version = ".".join(map(str, sys.version_info[0:2]))
    location = pathlib.Path(__file__).resolve().parents[1]
    message = f"pdfpop {__version__} from {location} (Python {python_version})"
    return message


if __name__ == "__main__":
    main()
