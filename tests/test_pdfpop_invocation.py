"""
Tests to make sure that pdfpop can be called from the cli without using the
entry point set up for the package.
"""

import os
import subprocess
import sys

import pytest


def test_module_should_invoke_main(monkeypatch):
    """Should produce pdfpop help message and exit with 0 code."""
    monkeypatch.setenv("PYTHONPATH", ".")

    result = subprocess.run(
        [sys.executable, "-m", "pdfpop", "-h"], capture_output=True
    )
    assert result.returncode == 0
    assert result.stdout.decode("utf-8").startswith("Usage: pdfpop")


def test_submodule_should_invoke_main(monkeypatch):
    """Should produce pdfpop help message and exit with 0 code."""
    monkeypatch.setenv("PYTHONPATH", ".")

    result = subprocess.run(
        [sys.executable, "-m", "pdfpop.cli", "-h"], capture_output=True
    )
    assert result.returncode == 0
    assert result.stdout.decode("utf-8").startswith("Usage: pdfpop")
