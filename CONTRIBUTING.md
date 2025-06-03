# Contributing to CompITA Report Generator

Thank you for your interest in contributing to the CompITA Report Generator project! This document provides guidelines and instructions for contributing to the project.

## Project Structure

The project follows a modular, maintainable structure:

```
compita-report-python/
│
├── compita/                      # Main package directory
│   ├── parsers/                  # Data parsing modules
│   ├── collectors/               # Data collection modules
│   ├── reports/                  # Report generation modules
│   ├── converters/               # Format conversion modules
│   ├── utils/                    # Utility modules
│   └── cli/                      # Command-line interface
│
├── bin/                          # Executable scripts
├── scripts/                      # Python scripts for specific tasks
├── static/                       # Static assets (images, CSS)
├── templates/                    # Report templates
├── docs/                         # Documentation
├── tests/                        # Test directory
├── assets/                       # Input data assets
└── reports/                      # Output reports
```

## Development Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd compita-report-python
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate     # On Windows
   ```

3. **Install the package in development mode:**

   ```bash
   pip install -e .
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for all functions, classes, and modules
- Keep functions small and focused on a single task
- Use meaningful variable and function names

## Adding New Features

1. **Create a new branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your feature:**
   - Add new modules to the appropriate directories
   - Update existing modules as needed
   - Add tests for your feature

3. **Document your feature:**
   - Update the relevant documentation files
   - Add docstrings to your code

4. **Submit a pull request:**
   - Ensure all tests pass
   - Ensure your code follows the coding standards
   - Provide a clear description of your changes

## Testing

- Write unit tests for all new functionality
- Run tests before submitting a pull request
- Ensure all tests pass

## Documentation

- Update documentation for any changes to the API
- Keep the README.md file up to date
- Add examples for new features

## Reporting Issues

- Use the issue tracker to report bugs
- Provide a clear description of the issue
- Include steps to reproduce the issue
- Include any relevant logs or error messages

## Code of Conduct

- Be respectful and inclusive
- Value constructive feedback
- Help others learn and grow

Thank you for your contributions!
