# CompITA Report Generator Developer Guide

This guide provides comprehensive instructions for developers working on the CompITA Report Generator project. It covers setting up a development environment, making and testing changes, building the standalone executable, and deploying updates.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Building the Standalone Executable](#building-the-standalone-executable)
- [Installing the Standalone Executable](#installing-the-standalone-executable)
- [Common Development Tasks](#common-development-tasks)
- [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites

- Python 3.9+ installed
- uv package manager (recommended) or pip

### Setting Up a Virtual Environment

Using uv (recommended):

```bash
# Navigate to the project directory
cd /path/to/compita-report-python

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install the package in development mode
uv pip install -e .
```

Using pip:

```bash
# Navigate to the project directory
cd /path/to/compita-report-python

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the package in development mode
pip install -e .
```

## Project Structure

The project follows a standard Python package structure:

```
compita-report-python/
├── compita/                  # Main package code
│   ├── cli/                  # CLI interface
│   ├── collectors/           # Data collection modules
│   ├── converters/           # Format conversion modules
│   ├── parsers/              # CSV parsing modules
│   └── reports/              # Report generation modules
├── scripts/                  # Utility scripts
├── build_scripts/            # Build-related scripts
├── docs/                     # Documentation
│   ├── api/                  # API reference
│   ├── cli/                  # CLI usage guides
│   ├── guides/               # User and developer guides
│   └── installation/         # Installation guides
├── assets/                   # Asset files
│   ├── comptia/              # Input CSV files
│   └── processed/            # Processed JSON files
├── reports/                  # Generated reports
├── compita-cli.py            # CLI entry point
├── setup.py                  # Package setup
└── requirements.txt          # Dependencies
```

## Development Workflow

### Making Changes

1. Activate your virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Make changes to the code using your preferred editor

3. Test your changes immediately using the development environment:
   ```bash
   python3 compita-cli.py generate-all --date YY-MM-DD
   ```

### Testing

The project uses a combination of manual testing and automated tests:

```bash
# Run unit tests
python -m unittest discover tests

# Test a specific command
python3 compita-cli.py generate-all --date YY-MM-DD
```

### JSON File Structure

The report generator relies on a specific JSON file structure in the `assets/processed/YY-MM-DD/` directory:

1. **Standardized JSON files** (required by most components):
   - `classgradebook.json` - Contains assessment data for all students
   - `studyhistory.json` - Contains study history data for all students
   - `timeperresource.json` - Contains time spent per resource for all students

2. **Original time-date format files** (preserved from CSV parsing):
   - `classgradebook-[time-date].json` (e.g., `classgradebook-5-05-5pm.json`)
   - `studyhistory-[time-date].json` (e.g., `studyhistory-05-05-4pm.json`)
   - `timeperresource-[time-date].json` (e.g., `timeperresource-05-05-5pm.json`)

3. **Adapter files** (used by flexible reports):
   - `assessment_data.json` - Reformatted assessment data
   - `study_history_data.json` - Reformatted study history data
   - `resource_time_data.json` - Reformatted resource time data

The system maintains both the standardized names and the original time-date format files to ensure compatibility with different components of the system. The standardized names are used by most components, while the original time-date format files are preserved for reference and backward compatibility.

**Important**: Avoid creating nested date directories (e.g., `assets/processed/YY-MM-DD/YY-MM-DD/`). All JSON files should be stored directly in the `assets/processed/YY-MM-DD/` directory.

## Building the Standalone Executable

Once you're satisfied with your changes, you can build the standalone executable:

```bash
# Activate your virtual environment
source .venv/bin/activate

# Run the build script
python3 build_scripts/build_standalone.py
```

This will create a standalone executable in the `build/output/compita-standalone.zip` file.

## Installing the Standalone Executable

You can install the standalone executable using the provided installation script:

```bash
# Run the installation script
./install_executable.sh
```

This script will:
1. Extract the ZIP file to a temporary location
2. Create the `~/bin` directory if it doesn't exist
3. Remove any existing `compita` executable or symlink
4. Copy the new executable to `~/bin`
5. Make it executable
6. Add `~/bin` to your PATH if it's not already there

### Manual Installation

If you prefer to install manually:

```bash
# Extract the ZIP file
unzip -o build/output/compita-standalone.zip -d /tmp/compita-temp

# Create bin directory if needed
mkdir -p ~/bin

# Copy executable
cp /tmp/compita-temp/compita ~/bin/

# Make it executable
chmod +x ~/bin/compita

# Ensure ~/bin is in PATH by adding to .zshrc
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Common Development Tasks

### Adding a New Command

1. Update the `create_parser` function in `compita/cli/commands.py` to add a new subparser
2. Create a new function to handle the command
3. Update the `run_command` function to call your new function

Example:

```python
def create_parser():
    # ... existing code ...
    
    # Add a new subparser for your command
    new_cmd_parser = subparsers.add_parser('new-command', help='Description of your new command')
    new_cmd_parser.add_argument('--option', help='Description of the option')
    
    # ... existing code ...

def new_command(args):
    """
    Implementation of your new command.
    
    Args:
        args: Command line arguments
    """
    print(f"Running new command with option: {args.option}")
    # Your implementation here

def run_command(args=None):
    # ... existing code ...
    
    # Add your command to the dispatch dictionary
    dispatch = {
        # ... existing commands ...
        'new-command': new_command,
    }
    
    # ... existing code ...
```

### Modifying the Report Generation Process

The report generation process consists of several steps:

1. Parsing CSV files to JSON
2. Generating flexible reports
3. Generating CSV module reports
4. Collecting and combining metrics
5. Generating markdown reports
6. Converting markdown to PDF

If you need to modify any of these steps, locate the corresponding function in the appropriate module and make your changes.

## Troubleshooting

### Common Issues

#### Missing Dependencies

If you encounter errors about missing dependencies:

```bash
# Install all dependencies
source .venv/bin/activate
uv pip install -e .
```

#### JSON File Structure Issues

If you encounter issues with the JSON file structure:

1. Check the output of the CSV parsing step
2. Verify that the JSON files are being created in the correct location
3. Ensure that the standardized names are being used

#### Parameter Conflicts

If you encounter parameter conflicts in function calls:

1. Check the function signature using `inspect.signature()`
2. Ensure that you're not passing the same parameter multiple times
3. Use keyword arguments (`**kwargs`) to pass only the parameters that the function accepts

#### Path Issues

If you encounter path-related issues:

1. Use absolute paths when possible
2. Ensure that all required directories exist before writing files
3. Use `os.makedirs(path, exist_ok=True)` to create directories

### Getting Help

If you need additional help:

1. Check the documentation in the `docs` directory
2. Look at the code comments for detailed explanations
3. Consult the project maintainers

## Conclusion

This developer guide should provide you with all the information you need to work on the CompITA Report Generator project. Remember to follow the established coding patterns and file structures to maintain consistency throughout the codebase.

Happy coding!
