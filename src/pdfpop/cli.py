"""CLI module for pdfpop."""
import pathlib
import sys

import click

import pdfpop
import pdfpop.commands


def version_msg() -> str:
    """Return the pdfpop version message string template."""
    python_version = ".".join(map(str, sys.version_info[0:2]))
    location = pathlib.Path(__file__).resolve().parents[1]
    return f"%(prog)s %(version)s from {location} (Python {python_version})"


@click.group(
    name="pdfpop", context_settings=dict(help_option_names=["-h", "--help"])
)
@click.version_option(
    pdfpop.__version__, "-V", "--version", message=version_msg()
)
def main() -> None:
    """Automate PDF population with pdfpop."""
    pass


@main.command()
@click.argument("form", type=click.Path(path_type=pathlib.Path, exists=True))
def config(form: pathlib.Path) -> None:
    """Generate a PDF form configuration file."""
    pdfpop.commands.config(form_path=form)


@main.command()
@click.argument("config", type=click.Path(path_type=pathlib.Path, exists=True))
@click.argument("data", type=click.Path(path_type=pathlib.Path, exists=True))
# @click.option("-o", "--output", default="populated.pdf", help="Output file path.")
def run(config: pathlib.Path, data: pathlib.Path) -> None:
    """Populate a PDF form with data as prescribed by the configuration file."""
    pdfpop.commands.run(config_path=config, data_path=data)


if __name__ == "__main__":
    main(prog_name="pdfpop")
