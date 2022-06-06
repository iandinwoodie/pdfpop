"""CLI module for pdfpop."""
import pathlib
import sys

import click

from pdfpop import __version__
from pdfpop.config import get_config, init_config
from pdfpop.main import pdfpop
from pdfpop.state import State
import pdfpop.commands as commands


def version_msg():
    """Return the pdfpop version message string template."""
    python_version = ".".join(map(str, sys.version_info[0:2]))
    location = pathlib.Path(__file__).resolve().parents[1]
    return f"%(prog)s %(version)s from {location} (Python {python_version})"


@click.group(name="pdfpop", context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-V", "--version", message=version_msg())
def main():
    """Automate PDF population with pdfpop."""
    pass


@main.command()
def list():
    """Lists all forms in the local library."""
    config = get_config()
    init_config(config)
    commands.list_forms(State(config))


@main.command()
@click.argument("name")
@click.argument("form", type=click.Path(path_type=pathlib.Path, exists=True))
@click.argument("description", required=False)
def add(name, form, description):
    """Add a form to the local library."""
    config = get_config()
    init_config(config)
    state = State(config)
    commands.add_form(state, config, form, name, description)
    state.save()


@main.command()
@click.argument("name")
def remove(name):
    """Remove a form from the local library."""
    config = get_config()
    init_config(config)
    state = State(config)
    commands.remove_form(state, config, name)
    state.save()


@main.command()
@click.argument("name")
@click.argument("data", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-o", "--output", default="populated.pdf", help="Output file path.")
def pop(name, data, output):
    """Populates a form with the specified data."""
    config = get_config()
    init_config(config)
    state = State(config)
    try:
        pdf = state.get_entry(name)["path"]
    except KeyError:
        print(f"Form {name} not found in library.")
        sys.exit(1)
    print(f'Populating "{output}" using form "{name}" and data "{data}"')
    pdfpop(in_path=pdf, data_path=data, out_path=output)


if __name__ == "__main__":
    main()
