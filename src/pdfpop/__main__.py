"""Allow pdfpop to be executable through `python -m pdfpop`."""
from pdfpop.cli import main


if __name__ == "__main__":
    main(prog_name="pdfpop")
