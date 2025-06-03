# CompITA Report Generator Web Interface

This document provides comprehensive documentation for the CompITA Report Generator web interface, including its features, pages, and usage instructions.

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Web Interface Pages](#web-interface-pages)
   - [Home Page & Dashboard](#home-page--dashboard)
   - [Generate Reports](#generate-reports)
   - [Upload CSV](#upload-csv)
   - [Available Reports](#available-reports)
   - [Flexible Reports](#flexible-reports)
   - [Setup Project](#setup-project)
4. [User Interface Components](#user-interface-components)
5. [Troubleshooting](#troubleshooting)

## Overview

The CompITA Report Generator web interface provides a user-friendly way to interact with the CompITA Report Generator system. It allows users to:

- Generate various types of reports
- Upload and parse CSV files
- View and download available reports
- Create and validate project structures
- Monitor system status through a dashboard

The web interface is built using HTML, CSS, and JavaScript with a Flask backend. It communicates with the CompITA API server to perform operations.

## Getting Started

### Starting the Web Interface

There are two ways to start the web interface:

1. **Web Interface Only**:
   ```
   python3 compita-cli.py web
   ```
   This starts only the web server. You'll need to start the API server separately.

2. **Complete Application (Recommended)**:
   ```
   python3 compita-cli.py app
   ```
   This starts both the web server and the API server, ensuring all functionality works properly.

By default, the web interface is available at http://localhost:8080.

### Configuration Options

When starting the web interface, you can specify several configuration options:

- `--host`: The host to bind the server to (default: 0.0.0.0)
- `--port`: The port to bind the server to (default: 8080)
- `--api-url`: The URL of the API server (default: http://localhost:8000)

Example with custom configuration:
```
python3 compita-cli.py web --host 127.0.0.1 --port 9090 --api-url http://api.example.com
```

## Web Interface Pages

### Home Page & Dashboard

The home page provides an overview of the system and quick access to all features. It includes:

- A dashboard showing recent projects and reports
- System status indicators (API server, storage)
- Quick access cards for all major functions

The dashboard automatically refreshes its status information and provides fallback content when the API server is unavailable.

### Generate Reports

The Generate Reports page allows you to generate all reports for a specific date. Features include:

- Date selection for the project
- One-click generation of all reports
- Task status monitoring with visual indicators
- Ability to check the status of previously submitted tasks

### Upload CSV

The Upload CSV page enables you to upload and parse CSV files for processing. Features include:

- File selection and upload
- Date specification for the uploaded data
- File type selection (assessment, resource_time, etc.)
- Parser type selection (standard, custom)
- Progress indicators during upload and processing

### Available Reports

The Available Reports page displays all generated reports for a selected date. Features include:

- Date selection to view reports
- Categorized display of reports by type
- Download links for each report
- File size and generation time information

### Flexible Reports

The Flexible Reports page allows you to generate customized reports with specific parameters. It includes three types of flexible reports:

1. **Flexible Module Reports**:
   - Select specific modules to include (1-14)
   - Specify subset modules for detailed analysis
   - Exclude specific modules from analysis
   - Option to count partial completions

2. **Flexible Assessment Reports**:
   - Select specific assessment types to include
   - Customize output file naming

3. **Flexible Grades Reports**:
   - Select grade categories to include
   - Specify custom weights for different grade components

### Setup Project

The Setup Project page allows you to create and validate project structures. Features include:

- Project creation with proper folder structure
- Date and class name specification
- Current module selection
- Required files selection
- Project validation with structural verification
- Visual display of the project directory structure

## User Interface Components

### Loading Indicators

The web interface includes several types of loading indicators to provide feedback during operations:

- Spinning loader for operations in progress
- Status indicators (running, completed, failed)
- Progress messages for multi-step operations

### Status Messages

Status messages provide feedback about operation results:

- Success messages with green indicators
- Warning messages with yellow indicators
- Error messages with red indicators and detailed information

### Form Validation

Forms include client-side validation to ensure proper input:

- Required field validation
- Date format validation
- Numeric input validation
- Immediate feedback on validation errors

## Troubleshooting

### API Connection Issues

If the dashboard shows "API Server: Not Configured" or "Offline":

1. Ensure the API server is running (`python3 compita-cli.py api`)
2. Check that the API URL is correctly configured
3. Verify there are no firewall or network issues blocking the connection

### Missing Reports or Projects

If reports or projects are not appearing in the interface:

1. Verify that the correct date format is being used (YY-MM-DD)
2. Check that the project structure is valid using the Setup Project page
3. Ensure all required CSV files have been uploaded and processed

### Browser Compatibility

The web interface is designed to work with modern browsers. If you experience display issues:

1. Try using the latest version of Chrome, Firefox, or Edge
2. Clear your browser cache and reload the page
3. Ensure JavaScript is enabled in your browser settings

### General Troubleshooting Steps

1. Restart both the API server and web server
2. Check the terminal output for error messages
3. Verify that all required dependencies are installed
4. Ensure you have proper permissions to read/write in the project directories
