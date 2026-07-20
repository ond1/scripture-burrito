# Building the Documentation

## Prerequisites

You need Python 3 and pip. To check:

```
python3 --version
pip --version
```

## Install dependencies

From the repository root:

```
pip install -r requirements.txt
```

This installs:
- **sphinx** — the documentation build engine
- **sphinx_rtd_theme** — the Read the Docs HTML theme
- **sphinx-jsonschema** — renders JSON schema files as documentation

Using a virtual environment is recommended:

```
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Build the HTML docs

```
cd docs
make html
```

The output is in `docs/_build/html/`. Open `docs/_build/html/index.html` in a browser to view it.
