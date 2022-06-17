"""Module for pdfpop commands."""
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
    print(f'Populating form "{form_cfg.data["io"]["form"]}".')
    data = _build_data_dict(data_path)
    if len(data) == 0:
        print("No entries found in data file. Exiting.")
        return
    elif len(data) > 1:
        print(
            "Multiple entries found in data file. Only the first will be used."
        )
    data = data[0]
    fields = _strip_field_type(form_cfg.data["fields"])
    mapped_data = build_mapped_data(data, fields)
    output_path = (
        pathlib.Path(form_cfg.data["io"]["output_dir"])
        / form_cfg.data["io"]["output_name"]
    )
    pdfpop.pdf.populate_form(
        form_cfg.data["io"]["form"], mapped_data, output_path
    )
    print(f'\nPopulated form saved to "{output_path}".')


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


def build_mapped_data(data, key_mapping):
    """Build a dictionary of data mapped to form fields."""

    def get_code_template() -> str:
        return "def fn(data):\n    %s\nrv = fn(data)\n"

    mapped_data = {}
    print("\nEvent Log:")
    ignore_list = []
    for key, value in key_mapping.items():
        if value is None:
            ignore_list.append(key)
        elif value in data:
            print(f'Set field "{key}" to "{data[value]}"')
            mapped_data[key] = data[value]
        else:
            global_env = {}
            local_env = {"data": data}
            full_expr = get_code_template() % value
            exec(full_expr, global_env, local_env)
            print(f'Set field "{key}" to "{local_env["rv"]}"')
            mapped_data[key] = local_env["rv"]
    for key in ignore_list:
        print(f'Ignored field "{key}"')
    return mapped_data
