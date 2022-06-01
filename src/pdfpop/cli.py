"""CLI module for pdfpop."""
import sys
import pathlib

import argparse
import pdfrw
import pandas as pd

from pdfpop import __version__


ANNOT_KEY = "/Annots"
ANNOT_FIELD_KEY = "/T"
ANNOT_VAL_KEY = "/V"
ANNOT_RECT_KEY = "/Rect"
SUBTYPE_KEY = "/Subtype"
WIDGET_SUBTYPE_KEY = "/Widget"


def main():
    """Main pdfpop function."""
    args = parse_cli()
    data = build_data_dict(args.excel)
    fill_pdf(args.pdf, args.out, data)


def parse_cli():
    """Load command line arguments."""
    parser = argparse.ArgumentParser(description="Populate PDF from Excel.")
    parser.add_argument("--version", action="version", version=version_msg())
    parser.add_argument("excel", help="Excel file to use as data source")
    parser.add_argument("pdf", help="PDF to be populated")
    parser.add_argument(
        "-o",
        "--out",
        help="Write output to file",
        default="populated.pdf",
        metavar="POPULATED",
    )
    return parser.parse_args()


def version_msg():
    """Return the pdfpop version, location, and Python powering it."""
    python_version = ".".join(map(str, sys.version_info[0:2]))
    location = pathlib.Path(__file__).resolve().parents[1]
    message = f"pdfpop {__version__} from {location} (Python {python_version})"
    return message


def build_data_dict(excel_file_path):
    """Build a dictionary of data to be used to populate the PDF."""
    df = pd.read_excel(excel_file_path, header=None, index_col=0)
    df = df.where(pd.notnull(df), None)
    return df.to_dict()[1]


def fill_pdf(input_pdf_path, output_pdf_path, data):
    """Fill the PDF with data and output at the specified path."""
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data.keys():
                        if isinstance(data[key], bool):
                            if data[key] is True:
                                annotation.update(
                                    pdfrw.PdfDict(AS=pdfrw.PdfName("Yes"))
                                )
                        else:
                            annotation.update(pdfrw.PdfDict(V="{}".format(data[key])))
                            annotation.update(pdfrw.PdfDict(AP=""))
    template_pdf.Root.AcroForm.update(
        pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true"))
    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


if __name__ == "__main__":
    main()
