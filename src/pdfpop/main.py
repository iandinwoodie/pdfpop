"""Main entry point for the `pdfpop` command."""
import pandas as pd
import pdfrw
import pathlib
import json
import ast

from pdfpop.config import get_config, init_config
from pdfpop.populator import single_form_fill

ANNOT_KEY = "/Annots"
ANNOT_FIELD_KEY = "/T"
ANNOT_VAL_KEY = "/V"
ANNOT_RECT_KEY = "/Rect"
SUBTYPE_KEY = "/Subtype"
WIDGET_SUBTYPE_KEY = "/Widget"
PARENT_KEY = "/Parent"


def pdfpop(in_path, data_path, out_path):
    """Run pdfpop just as if using it from the command line."""
    config = get_config()
    init_config(config)

    data = build_data_dict(data_path)
    if len(data) == 0:
        print("No data found in Excel file. Exiting.")
        return
    elif len(data) > 1:
        print("Muplite data rows found in Excel file. Only the first will be used.")
    data = data[0]
    with open(pathlib.Path(in_path).with_suffix(".json"), "r") as f:
        key_mapping = json.load(f)
    print("\nEvent Log:")
    mapped_data = build_mapped_data(data, key_mapping)
    single_form_fill(in_path, mapped_data, out_path)


def build_data_dict(data_path):
    """Build a dictionary of input data to be mapped to form fields."""
    df = pd.read_excel(data_path, header=0)
    df = df.where(pd.notnull(df), None).fillna("").astype(str)
    return df.to_dict("records")


CODE_TEMPLATE = """
def fn(data):
    %s
rv = fn(data)
"""


def build_mapped_data(data, key_mapping):
    """Build a dictionary of data mapped to form fields."""
    mapped_data = {}
    for key, container in key_mapping.items():
        if key == "ignored":
            for field in container:
                print(f'Ignore form field "{field}"')
        elif key == "col_mapping":
            for field, col in container.items():
                value = data[col]
                print(f'Populate form field "{field}" with "{value}"')
                mapped_data[field] = value
        elif key == "custom_mapping":
            for field, expr in container.items():
                global_env = {}
                local_env = {"data": data}
                full_expr = CODE_TEMPLATE % expr
                exec(full_expr, global_env, local_env)
                print(f'Populate form field "{field}" with "{local_env["rv"]}"')
                mapped_data[field] = local_env["rv"]
        else:
            raise RuntimeError(f'Unexpected key "{key}" found in JSON file.')
    return mapped_data


def get_form_fields(form_path):
    """Return a list of fields found in the given form."""
    pdf = pdfrw.PdfReader(form_path)
    fields = []
    for page in pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations is None:
            continue

        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if not annotation[ANNOT_FIELD_KEY]:
                    annotation = annotation[PARENT_KEY]
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY].to_unicode()
                    fields.append(key)
    return fields
