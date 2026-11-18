# dpl_screenshots

Python tools for working with screenshots.

## Setup

Create and activate a virtual environment, then install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.
On Debian/Ubuntu, if venv creation fails because `ensurepip` is unavailable,
install the matching `python3-venv` package first.

In the configured Bash shell on this workstation, entering this project
automatically activates `.venv`, and leaving the project deactivates it.

## Checks

Install the Git hooks once from the project root:

```bash
pre-commit install
```

Commits will run Ruff on Python files and the full pytest suite. To run both
hooks manually against the entire repository:

```bash
pre-commit run --all-files
```

The CLI entry point is available as `python -m dpl_screenshots.main` or,
after installing the project, `dpl-screenshots`. Both currently display help;
no screenshot-processing commands have been added yet.

## OCR dependency

`pytesseract` is a Python wrapper and also requires the Tesseract OCR executable
to be installed on the system and available on `PATH`.
