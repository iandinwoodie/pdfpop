"""PDF handling module for pdfpop."""
import pdfrw


def populate_form(in_pdf, data, suffix=None):
    fillers = {
        "checkbox": _checkbox,
        "list": _listbox,
        "text": _text_form,
        "combo": _combobox,
        "radio": _radio_button,
    }
    for page in in_pdf.pages:
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
                    fillers[ft](annotation, data[key])
                    if suffix:
                        new_T = pdfrw.objects.pdfstring.PdfString.encode(
                            key + suffix
                        )
                        annotation.update(pdfrw.PdfDict(T=new_T))
        in_pdf.Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true"))
        )
    return in_pdf


def _text_form(annotation, value):
    pdfstr = pdfrw.objects.pdfstring.PdfString.encode(value)
    annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr, AP=""))


def _checkbox(annotation, value):
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


RADIO_BUTTON_CACHE = {}


def _radio_button(annotation, value):
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


def _combobox(annotation, value):
    export = None
    for each in annotation["/Opt"]:
        if each[1].to_unicode() == value:
            export = each[0].to_unicode()
    if export is None:
        raise KeyError(f"Export Value: {value} Not Found")
    pdfstr = pdfrw.objects.pdfstring.PdfString.encode(export)
    annotation.update(pdfrw.PdfDict(V=pdfstr, AS=pdfstr, AP=""))


def _listbox(annotation, values):
    print(annotation)
    field = annotation["/T"].to_unicode()
    print(f'Populate combobox "{field}" with "{values}"')
    pdfstrs = []
    for value in values:
        export = None
        for each in annotation["/Opt"]:
            print(each)
            if each[1].to_unicode() == value:
                export = each[0].to_unicode()
        if export is None:
            raise KeyError(f"Export Value: {value} Not Found")
        pdfstrs.append(pdfrw.objects.pdfstring.PdfString.encode(export))
    empty = []
    for each in pdfstrs:
        print(each)
        empty.append("")
    annotation.update(pdfrw.PdfDict(V=pdfstrs, AS=pdfstrs, AP=empty))


def _field_type(annotation):
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


