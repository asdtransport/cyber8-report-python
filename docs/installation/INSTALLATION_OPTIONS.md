# CompITA Report Generator - Installation & Usage Options

This document explains the different ways to install and use the CompITA Report Generator.

## Installation Options

The CompITA Report Generator can be installed and used in three different ways:

1. Standard Python Package Installation
2. Global CLI Access
3. Standalone Executable

Each option has its own advantages and use cases, as explained below.

## 1. Standard Python Package Installation

**Files involved:**
- `setup.py`: Defines package metadata, dependencies, and installation configuration
- `install.sh`: Convenience script to install the package in development mode

This approach allows users to install the package using standard Python methods:

```bash
# Install from local directory
pip install .

# Or, if published to PyPI
pip install compita-report-generator
```

**Advantages:**
- Follows standard Python package conventions
- Easy to update with pip
- Integrates with Python ecosystem

**Disadvantages:**
- Requires Python to be installed
- Requires all dependencies (pandas, etc.) to be installed
- May encounter issues with externally managed Python environments

## 2. Global CLI Access

**Files involved:**
- `compita-cli`: Main CLI script that handles commands and arguments
- `compita-global`: Launcher script that allows running the CLI from anywhere
- `GLOBAL_CLI_USAGE.md`: Documentation explaining how to use the global CLI

This setup allows users to run the CompITA CLI from any directory by adding the script to their PATH:

```bash
# Add to PATH (usually in .bashrc or .zshrc)
export PATH="/path/to/compita-report-python:$PATH"

# Then use from anywhere
compita-global generate-all --date 25-05-05
```

**Advantages:**
- Run from any directory without specifying the full path
- No need to be in the project directory
- Convenient for frequent use

**Disadvantages:**
- Still requires Python and dependencies to be installed
- Requires modifying PATH environment variable

## 3. Standalone Executable

**Files involved:**
- `build_standalone.py`: Script to build a self-contained executable with all dependencies
- `compita-standalone.zip`: The resulting standalone package

This approach bundles everything (including pandas and all other dependencies) into a single executable:

```bash
# Extract the standalone package
unzip compita-standalone.zip -d compita-standalone

# Navigate to the extracted directory
cd compita-standalone

# Run the executable
./compita generate-all --date 25-05-05
```

**Advantages:**
- No Python installation required
- All dependencies bundled in one package
- Works on any compatible system without additional setup
- Ideal for distribution to end users

**Disadvantages:**
- Larger file size
- Less flexible for development
- Needs to be rebuilt when code changes

## Project Structure Overview

The project has a well-organized structure:

```
compita-report-python/
├── compita/                   # Main package directory
│   ├── cli/                   # CLI implementation
│   │   ├── commands.py        # Command definitions
│   │   ├── interactive.py     # Interactive mode
│   │   └── main.py            # Main entry point
│   ├── parsers/               # Data parsers
│   │   └── csv_parser.py      # CSV parsing functionality
│   └── reports/               # Report generators
│       └── flexible_module.py # Flexible module reports
├── assets/                    # Assets directory
│   ├── comptia/               # Input CSV files
│   └── processed/             # Processed JSON files
├── compita-cli                # CLI script
├── compita-global             # Global launcher
├── setup.py                   # Package setup
├── build_standalone.py        # Standalone build script
├── install.sh                 # Installation script
└── GLOBAL_CLI_USAGE.md        # Usage documentation
```

## Recommended Approach

For end users who just want to use the tool without any setup, the **Standalone Executable** option is recommended.

For developers working on the codebase, the **Standard Python Package Installation** with the `install.sh` script is the most appropriate.

For regular users who have Python installed and want convenient access, the **Global CLI** option provides a good balance.
