"""Module for pdfpop state."""
import datetime
import json


class State:
    """State class."""

    def __init__(self, config_path):
        """Initialize State."""
        self.path = config_path["data_path"] / "state.json"
        self.data = self.load()

    def load(self):
        """Load State."""
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save(self):
        """Save State."""
        with open(self.path, "w") as f:
            json.dump(self.data, f)
        pass

    def get_entries(self):
        """Get entries from State."""
        return self.data

    def get_entry(self, name):
        """Get entry from State."""
        return self.data[name]

    def add_entry(self, name, path, config, desc):
        """Add entry to State."""
        self.data[name] = {
            "desc": desc,
            "path": path,
            "config": config,
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def remove_entry(self, name):
        """Get entry from State."""
        del self.data[name]
