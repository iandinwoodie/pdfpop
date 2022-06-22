"""Form configuration handling for pdfpop."""
from __future__ import annotations
from typing import Any
import json
import pathlib


class FormConfig:
    """Representation of a form configuration."""

    def __init__(self, config_path: pathlib.Path) -> None:
        """Initialize the form configuration."""
        self._path = config_path
        self._data = {
            "io": {
                "form": None,
                "output_dir": None,
                "output_name": None,
            },
            "fields": {},
        }

    @property
    def path(self) -> pathlib.Path:
        """Configuration path getter."""
        return self._path

    @property
    def data(self) -> dict[str, dict[str, Any]]:
        """Configuration data getter."""
        return self._data

    def exists(self) -> bool:
        """Return whether the configuration exists."""
        return self._path.exists()

    def save(self) -> None:
        """Save the configuration to disk."""
        with self._path.open("w") as f:
            json.dump(self._data, f, indent=4)

    def load(self) -> None:
        """Load the configuration from disk."""
        with self._path.open() as f:
            self._data = json.load(f)


def get_default_path(form_path: pathlib.Path) -> pathlib.Path:
    """Return the default configuration path for the specified form."""
    return pathlib.Path().cwd() / f"pdfpop-{form_path.stem}.json"


def interpret(
    section: dict[str, Any], data: dict[str, Any], verbose: bool = False
) -> dict[str, Any]:
    """Interpret the configuration section."""

    def wrap_logic(logic: str) -> str:
        """Returns a function wrapping the given logic."""
        if "return" in logic:
            return f"def fn(data):\n    {logic}\nrv = fn(data)\n"
        return f"rv = {logic}\n"

    interpreted = {}
    ignore_list = []
    for key, value in section.items():
        if value is None:
            ignore_list.append(key)
            continue
        elif value in data:
            interpreted[key] = data[value]
        elif isinstance(value, int) or isinstance(value, float):
            interpreted[key] = value
        else:
            global_env = {}
            local_env = {"data": data, "rv": None}
            expr = wrap_logic(value)
            try:
                exec(expr, global_env, local_env)
            except Exception as e:
                pass
            interpreted[key] = (
                local_env["rv"] if local_env["rv"] is not None else value
            )
        if verbose:
            print(f'Set field "{key}" to "{interpreted[key]}"')
    if verbose:
        for key in ignore_list:
            print(f'Ignored field "{key}"')
    return interpreted
