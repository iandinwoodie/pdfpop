<p align="center">
  <img src="assets/images/pdfpop-banner.png"
      alt="Automate PDF population with pdfpop"
      title="pdfpop" />
</p>

[![License](https://img.shields.io/github/license/iandinwoodie/pdfpop)](LICENSE.txt)
[![Release](https://img.shields.io/github/v/tag/iandinwoodie/pdfpop)](https://github.com/iandinwoodie/pdfpop/releases)
[![CI/CD Tests](https://github.com/iandinwoodie/pdfpop/actions/workflows/tests.yml/badge.svg)](https://github.com/iandinwoodie/pdfpop/actions/workflows/tests.yml)
[![Codecov](https://codecov.io/gh/iandinwoodie/pdfpop/branch/main/graph/badge.svg?token=ZNY5FIHA9U)](https://codecov.io/gh/iandinwoodie/pdfpop)
[![Size](https://img.shields.io/github/repo-size/iandinwoodie/pdfpop)](https://github.com/iandinwoodie/pdfpop)

---

Automate PDF population with pdfpop.

## Installation

You can install `pdfpop` with:

```bash
pip install pdfpop
```

## Usage

The `pdfpop` usage consists of two steps: (1) form configuration and (2)
execution.

### Step 1. Form Configuration

> ℹ️  This step only needs to be run once for each unique form.

This step generates a form-specific configuration file that allows you to inform
`pdfpop` how data should be routed from the data file to the PDF form. You can
generate this file with the `config` command:

```bash
# Usage: pdfpop config <form>
pdfpop config examples/example-form.pdf
```

This will output a `pdfpop-` prefixed JSON file in your current working
directory (e.g., `pdfpop-example-form.json`). By default, all fields will be
assigned a value of `null` and, therefore, will be ignored until the `null`
value is replaced with instructions on how to populate the field. An example of
an edited configuration file is available [here](examples/example-form.json).

### Step 2. Exectuion

Once you have a form configuration file you can populate your PDF form using the
`run` command:

```bash
# Usage: pdfpop run <config> <data>
pdfpop run examples/example-form.json examples/example-data.xlsx
```

This will generate a populated PDF form at the location prescribed by the values
of`<output_dir>/<output_name>` in the configuration file (e.g.,
`examples/pdfpop-example-form.pdf`).

# License

Copyright (C) 2022 Ian Dinwoodie

* Licensed under [GNU General Public License v3.0](LICENSE.txt).
* Exceptions:
    * Material covered by [Third Party Licenses](LICENSE-THIRD-PARTY.txt).
    * Logo icon: <a href="https://www.flaticon.com/free-icons/popsicle-stick" title="popsicle stick icons">Popsicle stick icons created by Freepik - Flaticon</a>
