# CompITA Report Generator Installation Guide

This guide explains how to install the CompITA Report Generator package with all its dependencies.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/compita-report-python.git
   cd compita-report-python
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

   This will install the package and all its dependencies, including pandas, numpy, weasyprint, etc.

3. Verify the installation:
   ```bash
   compita --help
   ```

### Method 2: Create a Virtual Environment (Recommended for Isolated Installation)

1. Create a virtual environment:
   ```bash
   python -m venv compita-venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     compita-venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source compita-venv/bin/activate
     ```

3. Install the package:
   ```bash
   cd compita-report-python
   pip install -e .
   ```

4. Verify the installation:
   ```bash
   compita --help
   ```

### Method 3: Install with uv (Faster Installation)

1. Install uv if you don't have it:
   ```bash
   pip install uv
   ```

2. Install the package using uv:
   ```bash
   cd compita-report-python
   uv pip install -e .
   ```

3. Verify the installation:
   ```bash
   compita --help
   ```

## Usage

After installation, you can use the CompITA CLI in two ways:

### Command-line Mode

```bash
compita generate-all --date 25-05-05 --assets-dir /path/to/assets
```

### Interactive Mode

```bash
compita --interactive
```

## Troubleshooting

If you encounter the error "pandas is required for CSV parsing", it means the dependencies weren't properly installed. Try reinstalling the package with:

```bash
pip install -e .
```

Or install pandas directly:

```bash
pip install pandas
```

## For Package Maintainers

To build a distribution package:

```bash
pip install build
python -m build
```

This will create both a source distribution (.tar.gz) and a wheel (.whl) in the dist/ directory.
