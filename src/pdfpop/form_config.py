"""Form configuration handling for pdfpop."""
import pathlib
import json


def get_default_path(form_path: pathlib.Path) -> pathlib.Path:
    """Return the default configuration path for the specified form."""
    return pathlib.Path().cwd() / f"pdfpop-{form_path.stem}.json"


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
    def data(self) -> dict[str, dict[str, str]]:
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
