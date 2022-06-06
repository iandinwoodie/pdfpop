"""Configuration handling for pdfpop."""
import pathlib


DEFAULT_CONFIG = {
    "config_path": pathlib.Path.home() / ".config" / "pdfpop",
    "data_path": pathlib.Path.home() / ".local" / "share" / "pdfpop",
}


def get_config():
    """Get the configuration."""
    return DEFAULT_CONFIG


def init_config(config):
    """Initialize the configuration directories."""
    config_path = config["config_path"]
    data_path = config["data_path"]
    if not config_path.exists():
        print(f'Creating configuration directory "{config_path}"')
        config_path.mkdir(parents=True)
    if not data_path.exists():
        print(f'Creating data directory "{data_path}"')
        data_path.mkdir(parents=True)
