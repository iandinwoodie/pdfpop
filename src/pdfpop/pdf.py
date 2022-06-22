"""PDF handling module for pdfpop.

Contains adaptations from:
* WestHealth/pdf-form-filler (https://github.com/WestHealth/pdf-form-filler)
    * Copyright (c) 2021, West Health Institute
"""
import pathlib

import pdfrw


def get_fields_info(form_path: pathlib.Path) -> dict[str, str]:
    """Return a list of field info for a form."""
    form = pdfrw.PdfReader(form_path)
    return _iterate_pages(form)


def populate_form(
    form_path: pathlib.Path, data: dict, output_path: pathlib.Path
) -> None:
    """Populate a PDF form with data and output to a new PDF."""
    form = pdfrw.PdfReader(form_path)
    strategies = _get_strategies()
    for page in form.pages:
        annotations = page["/Annots"]
        if annotations is None:
            continue
        for annotation in annotations:
            if annotation["/Subtype"] == "/Widget":
                if not annotation["/T"]:
                    annotation = annotation["/Parent"]
                key = annotation["/T"].to_unicode()
                if key in data:
                    ft = _field_type(annotation)
                    strategies[ft](annotation, data[key])
        form.Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true"))
        )
    pdfrw.PdfWriter().write(output_path, form)


def _iterate_pages(form: pdfrw.pdfreader.PdfReader) -> dict[str, str]:
    """Iterate through pages in a form."""
    fields_info = {}
    for page in form.pages:
        _iterate_annotations(page, fields_info)
    return fields_info


def _iterate_annotations(
    page: pdfrw.objects.pdfdict.PdfDict, fields_info: dict[str, str]
) -> None:
    """Iterate through annotations on a page."""
    annotations = page["/Annots"]
    for annotation in annotations:
        if annotation["/Subtype"] != "/Widget":
            continue
        if not annotation["/T"]:
            annotation = annotation["/Parent"]
        key = annotation["/T"].to_unicode()
        ft = _field_type(annotation)
        fields_info[f"{key} [{ft}]"] = None


def _field_type(annotation) -> str:
    """Return the field type of an annotation."""
    ft = annotation["/FT"]
    ff = annotation["/Ff"]
    if ft == "/Tx":
        return "text"
    if ft == "/Ch":
        if ff and int(ff) & 1 << 17:  # test 18th bit
            return "combo"
        else:
            return "list"
    if ft == "/Btn":
        if ff and int(ff) & 1 << 15:  # test 16th bit
            return "radio"
        else:
            return "checkbox"


def _get_strategies() -> dict:
    """Return a dictionary of field type to strategy function."""
    return {
        "checkbox": _checkbox_strategy,
        "combo": _combo_box_strategy,
        "list": _list_box_strategy,
        "radio": _radio_button_strategy,
        "text": _text_box_strategy,
    }


def _checkbox_strategy(annotation, value) -> None:
    if not isinstance(value, bool):
        orig_value = value
        value = value.lower() in [
            "x",
            "true",
            "t",
            "yes",
            "y",
            "on",
            "check",
            "checked",
        ]
        field = annotation["/T"].to_unicode()
        print(f'Treat "{orig_value}" as "{value}" for field "{field}"')
    if value:
        val_str = pdfrw.objects.pdfname.BasePdfName("/Yes")
    else:
        val_str = pdfrw.objects.pdfname.BasePdfName("/Off")
    annotation.update(pdfrw.PdfDict(V=val_str))


def _combo_box_strategy(annotation, value) -> None:
    export = None
    for each in annotation["/Opt"]:
        if each[1].to_unicode() == value:
            export = each[0].to_unicode()
    if export is None:
        raise KeyError(f"Export Value: {value} Not Found")
    pdfstr = pdfrw.objects.pdfstring.PdfString.encode(export)
    annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr, AP=""))


def _list_box_strategy(annotation, values) -> None:
    field = annotation["/T"].to_unicode()
    pdfstrs = []
    for value in values:
        export = None
        for each in annotation["/Opt"]:
            if each[1].to_unicode() == value:
                export = each[0].to_unicode()
        if export is None:
            raise KeyError(f"Export Value: {value} Not Found")
        pdfstrs.append(pdfrw.objects.pdfstring.PdfString.encode(export))
    empty = ["" for _ in range(len(pdfstrs))]
    annotation.update(pdfrw.PdfDict(V=pdfstrs, AS=pdfstrs, AP=empty))


RADIO_BUTTON_CACHE = {}


def _radio_button_strategy(annotation, value) -> None:
    field = annotation["/T"].to_unicode()
    if field in RADIO_BUTTON_CACHE:
        return
    else:
        RADIO_BUTTON_CACHE[field] = True
    for each in annotation["/Kids"]:
        # determine the export value of each kid
        keys = each["/AP"]["/N"].keys()
        if ["/Off"] in keys:
            keys.remove("/Off")
        export = keys[0]

        if f"/{value}" == export:
            val_str = pdfrw.objects.pdfname.BasePdfName(f"/{value}")
        else:
            val_str = pdfrw.objects.pdfname.BasePdfName(f"/Off")
        each.update(pdfrw.PdfDict(AS=val_str))
    annotation.update(
        pdfrw.PdfDict(V=pdfrw.objects.pdfname.BasePdfName(f"/{value}"))
    )


def _text_box_strategy(annotation, value) -> None:
    pdfstr = pdfrw.objects.pdfstring.PdfString.encode(value)
    annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr, AP=""))
