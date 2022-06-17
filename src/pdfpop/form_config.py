"""Form configuration handling for pdfpop."""
import pathlib


def get_default_path(form_path: pathlib.Path) -> pathlib.Path:
    """Return the default configuration path for the specified form."""
    return pathlib.Path().cwd() / f"pdfpop-{form_path.stem}.json"


class FormConfig:
    """Representation of a form configuration."""

    def __init__(self, config_path: pathlib.Path) -> None:
        """Initialize the form configuration."""
        self._config_path = config_path
        self._data = {}

    def exists(self) -> bool:
        """Return whether the configuration exists."""
        return self._config_path.exists()
