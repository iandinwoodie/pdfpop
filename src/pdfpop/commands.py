"""Module for pdfpop commands."""
import pathlib
import shutil
import json

from pdfpop.main import get_form_fields


def list_forms(state):
    """List all pdfs in the local library."""
    entries = state.get_entries()
    if not len(entries):
        print("No forms in the local library.")
    else:
        for key, entry in entries.items():
            print(f'{key}: {entry["desc"]} (config: {entry["config"]})')


def add_form(state, config, form, name, description):
    """Add the specified form to the local library."""
    local_path = config["data_path"] / name
    local_path = local_path.with_suffix(".pdf")
    shutil.copy(form, local_path)
    form_config_path = dump_form_config(local_path)
    state.add_entry(name, str(local_path), str(form_config_path), description)
    print(f'Added form "{name}" to the local library.')


def dump_form_config(form_path):
    """Dump a form config for the given form."""
    config = {
        "col_mapping": {},
        "custom_mapping": {},
        "ignored": get_form_fields(form_path),
    }
    form_config_path = form_path.with_suffix(".json")
    with open(form_config_path, "w") as f:
        json.dump(config, f, indent=4)
    return form_config_path


def remove_form(state, config, name):
    """Remove the specified form from the local library."""
    try:
        entry = state.get_entry(name)
        state.remove_entry(name)
        local_path = pathlib.Path(entry["path"])
        local_path.unlink()
        local_config_path = local_path.with_suffix(".json")
        local_config_path.unlink()
        print(f'Removed form "{name}" from the local library.')
    except KeyError:
        print(f'Form "{name}" not found in the local library.')
