"""Main entry point for the `pdfpop` command."""
import pandas as pd
import pdfrw

ANNOT_KEY = "/Annots"
ANNOT_FIELD_KEY = "/T"
ANNOT_VAL_KEY = "/V"
ANNOT_RECT_KEY = "/Rect"
SUBTYPE_KEY = "/Subtype"
WIDGET_SUBTYPE_KEY = "/Widget"


def pdfpop(input_pdf_path, input_excel_path, output_pdf_path):
    """Run pdfpop just as if using it from the command line."""
    data = build_data_dict(input_excel_path)
    fill_pdf(input_pdf_path, output_pdf_path, data)


def build_data_dict(input_excel_path):
    """Build a dictionary of data to be used to populate the PDF."""
    df = pd.read_excel(input_excel_path, header=None, index_col=0)
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
