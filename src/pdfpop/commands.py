"""Module for pdfpop commands."""
import errno
import os
import pathlib

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
    return
