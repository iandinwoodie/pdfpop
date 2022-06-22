"""Module for pdfpop commands."""
from typing import Any
import errno
import os
import pathlib

import pandas as pd

import pdfpop.form_config
import pdfpop.pdf


def config(form_path: pathlib.Path) -> None:
    """Generate a form configuration file."""
    if not form_path.exists():
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), str(form_path)
        )
    form_cfg = pdfpop.form_config.FormConfig(
        pdfpop.form_config.get_default_path(form_path)
    )
    if form_cfg.exists():
        raise FileExistsError(
            errno.EEXIST, os.strerror(errno.EEXIST), str(form_cfg.path)
        )
    form_cfg.data["io"]["form"] = str(form_path.resolve())
    form_cfg.data["io"]["output_dir"] = str(pathlib.Path.cwd())
    form_cfg.data["io"]["output_name"] = str(f"pdfpop-{form_path.stem}.pdf")
    form_cfg.data["fields"] = pdfpop.pdf.get_fields_info(form_path)
    form_cfg.save()
    print(f'Generated form configuration file "{form_cfg.path}".')


def run(config_path: pathlib.Path, data_path: pathlib.Path) -> None:
    """Generate a populated PDF file."""
    if not config_path.exists():
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), str(config_path)
        )
    form_cfg = pdfpop.form_config.FormConfig(config_path)
    form_cfg.load()
    data = _build_data_dict(data_path)
    if len(data) == 0:
        print("No entries found in data file. Exiting.")
        return
    fields = _strip_field_type(form_cfg.data["fields"])
    for idx, row in enumerate(data):
        io = pdfpop.form_config.interpret(form_cfg.data["io"], row)
        form_path = pathlib.Path(io["form"])
        print(f'\nPopulating form "{form_path}" for row {idx+1}.')
        row_fields = pdfpop.form_config.interpret(
            form_cfg.data["fields"], row, verbose=True
        )
        output_path = pathlib.Path(io["output_dir"]) / io["output_name"]
        _run_single_row(form_path, row_fields, output_path)
        print(f'Populated form saved to "{output_path}".')


def _build_data_dict(data_path: pathlib.Path) -> dict:
    """Build a data frame from a CSV file."""
    if not data_path.exists():
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), str(data_path)
        )
    if data_path.suffix in [".xls", ".xlsx"]:
        df = pd.read_excel(data_path, header=0)
        df = df.where(pd.notnull(df), None).fillna("").astype(str)
        return df.to_dict("records")
    else:
        raise RuntimeError("Unsupported data file type: {data_path.suffix}.")


def _strip_field_type(fields: dict[str, str]) -> dict[str, str]:
    """Strip the bracket enclosed field type from the field name."""
    return {k.split(" [")[0]: v for k, v in fields.items()}


def _run_single_row(
    form: pathlib.Path, row: dict[str, Any], output_path: pathlib.Path
) -> None:
    """Run a single row of data."""
    pdfpop.pdf.populate_form(form, row, output_path)
