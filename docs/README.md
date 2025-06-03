# CompITA Report Generator Documentation

This directory contains comprehensive documentation for the CompITA Report Generator.

## Table of Contents

### CLI Documentation
- [CLI Usage Guide](cli/CLI_USAGE.md) - How to use the CompITA CLI
- [Global CLI Usage Guide](cli/GLOBAL_CLI_USAGE.md) - How to use the CompITA CLI globally from anywhere on your system

### Installation Documentation
- [Installation Guide](installation/INSTALL.md) - How to install the CompITA Report Generator
- [Installation Options](installation/INSTALLATION_OPTIONS.md) - Different ways to install and use the CompITA Report Generator

### API Documentation
- [API Reference](api/README.md) - Reference documentation for the CompITA Report Generator API
- [API Usage Guide](api/API_USAGE.md) - How to use the API and web interface
- [API Endpoints](api/ENDPOINTS.md) - Detailed documentation of all API endpoints

### Web Interface Documentation
- [Web Interface Guide](web/README.md) - Comprehensive guide to the web interface
- [Web Pages Documentation](web/PAGES.md) - Detailed documentation of each web page
- [Technical Guide](web/TECHNICAL.md) - Technical details of the web interface architecture

### Deployment Documentation
- [Railway Deployment Guide](deployment/RAILWAY.md) - How to deploy the CompITA Report Generator to Railway

## Project Structure

The CompITA Report Generator is organized as follows:

```
compita-report-python/
├── compita/                   # Main package code
│   ├── src/                   # Source code for API and web interface
│   │   ├── api/               # FastAPI implementation
│   │   └── web/               # Web interface files
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
│   ├── cli/                   # CLI documentation
│   ├── installation/          # Installation guides
│   └── api/                   # API documentation
├── tests/                     # Test suite
├── build_scripts/             # Build-related scripts
├── assets/                    # Assets directory
├── compita-cli                # Main CLI entry point
├── compita-global             # Global CLI launcher
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
└── README.md                  # Project overview
```

## Building the Package

To build a standalone executable package:

```bash
./build_scripts/build_standalone.py
```

The output will be placed in the `build/output` directory, with the final package at `build/output/compita-standalone.zip`.
