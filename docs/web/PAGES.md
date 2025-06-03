# Web Interface Pages Documentation

This document provides detailed information about each page in the CompITA Report Generator web interface.

## Table of Contents

1. [Home Page & Dashboard](#home-page--dashboard)
2. [Generate Reports Page](#generate-reports-page)
3. [Upload CSV Page](#upload-csv-page)
4. [Available Reports Page](#available-reports-page)
5. [Flexible Reports Page](#flexible-reports-page)
6. [Setup Project Page](#setup-project-page)

## Home Page & Dashboard

The home page serves as the central hub for the CompITA Report Generator web interface. It provides quick access to all features and includes a dashboard with real-time information.

### Dashboard Components

1. **Recent Projects Panel**
   - Displays the 5 most recent projects (by date)
   - Shows project date and class name (if available)
   - Provides quick links to edit project settings or generate reports

2. **Recent Reports Panel**
   - Lists the 5 most recently generated reports
   - Shows report type and date
   - Includes direct links to view the reports

3. **System Status Panel**
   - API Server status (Online, Degraded, Offline)
   - Storage status with usage information
   - Last updated timestamp

### Feature Cards

The home page includes feature cards for quick access to all major functions:

- Generate Reports
- Upload CSV
- Available Reports
- Flexible Reports
- Setup Project

Each card includes a brief description and a direct link to the corresponding page.

### Technical Details

- The dashboard automatically refreshes system status information every minute
- Local storage is used to cache project and report information for faster loading
- Fallback mechanisms ensure the dashboard remains useful even when the API is unavailable

## Generate Reports Page

The Generate Reports page allows users to generate all reports for a specific project date.

### Features

1. **Date Selection**
   - Input field for selecting the project date (YY-MM-DD format)
   - Validation to ensure the date format is correct

2. **Generation Controls**
   - "Generate All Reports" button to start the report generation process
   - "Check Status" button to check the status of a previously submitted task

3. **Task Status Display**
   - Visual indicator showing the current status (running, completed, failed)
   - Detailed status message describing the current operation
   - Task ID reference for tracking purposes

### Usage Instructions

1. Enter a valid project date in YY-MM-DD format
2. Click "Generate All Reports" to start the generation process
3. Monitor the task status as reports are generated
4. Once completed, use the "Available Reports" page to access the generated reports

### Technical Details

- The generation process runs as a background task on the API server
- Status updates are polled every 2 seconds during generation
- The process includes parsing CSV files, collecting metrics, and generating all report types

## Upload CSV Page

The Upload CSV page enables users to upload and parse CSV files for processing.

### Features

1. **File Selection**
   - File input for selecting CSV files from your local system
   - Support for all CompITA CSV file formats

2. **Upload Configuration**
   - Date field for specifying the project date (YY-MM-DD format)
   - File type selection (assessment, resource_time, etc.)
   - Parser type selection (standard, custom)

3. **Upload Status**
   - Progress indicator during file upload and processing
   - Status messages showing the current operation
   - Completion notification with next steps

### Supported File Types

- **assessment**: Assessment data CSV files
- **resource_time**: Resource time data CSV files
- **gradebook**: Gradebook data CSV files
- **study_history**: Study history data CSV files

### Usage Instructions

1. Select a CSV file from your local system
2. Enter the project date in YY-MM-DD format
3. Select the appropriate file type and parser type
4. Click "Upload and Parse" to start the process
5. Wait for the upload and parsing to complete

### Technical Details

- Files are uploaded directly to the API server for processing
- The parser converts CSV data to JSON format for further processing
- Processed files are stored in the project's processed directory

## Available Reports Page

The Available Reports page displays all generated reports for a selected project date and provides download links.

### Features

1. **Date Selection**
   - Input field for selecting the project date (YY-MM-DD format)
   - "Load Reports" button to fetch reports for the selected date

2. **Reports Display**
   - Categorized sections for different report types
   - File name, type, and size information for each report
   - Direct download links for each report

3. **Report Categories**
   - Student Reports (individual student performance reports)
   - Class Reports (overall class performance reports)
   - Module Reports (performance data by module)
   - Flexible Reports (custom reports with specific parameters)

### Usage Instructions

1. Enter a valid project date in YY-MM-DD format
2. Click "Load Reports" to fetch available reports
3. Browse the categorized report listings
4. Click the download link for any report you wish to access

### Technical Details

- Report listings are fetched from the API server based on the selected date
- File sizes are displayed in human-readable format (KB, MB)
- Downloads are handled directly by the browser

## Flexible Reports Page

The Flexible Reports page allows users to generate customized reports with specific parameters.

### Flexible Module Reports

This section allows you to generate module-specific reports with custom parameters.

#### Features

- Date selection for the project (YY-MM-DD format)
- Module selection options:
  - All Modules: Select which modules (1-14) to include in the overall analysis
  - Subset Modules: Select specific modules for detailed analysis
  - Exclude Modules: Select modules to exclude from the analysis
- Count Partial option to count partial completions as fully completed
- Output prefix field for custom file naming

#### Usage Instructions

1. Enter the project date in YY-MM-DD format
2. Select the modules to include in the "All Modules" section
3. Optionally select subset modules or exclude modules
4. Set the "Count Partial" option if desired
5. Enter an output prefix for the report file name
6. Click "Generate Flexible Module Report" to create the report

### Flexible Assessment Reports

This section allows you to generate assessment-specific reports with custom parameters.

#### Features

- Date selection for the project (YY-MM-DD format)
- Assessment type selection (quizzes, exams, assignments, etc.)
- Module selection for specific modules to include
- Output prefix field for custom file naming

#### Usage Instructions

1. Enter the project date in YY-MM-DD format
2. Select the assessment types to include
3. Optionally select specific modules to include
4. Enter an output prefix for the report file name
5. Click "Generate Flexible Assessment Report" to create the report

### Flexible Grades Reports

This section allows you to generate grade reports with custom weighting.

#### Features

- Date selection for the project (YY-MM-DD format)
- Grade category selection (quizzes, exams, assignments, etc.)
- Custom weight inputs for each selected category
- Module selection for specific modules to include
- Output prefix field for custom file naming

#### Usage Instructions

1. Enter the project date in YY-MM-DD format
2. Select the grade categories to include
3. Enter custom weights for each selected category
4. Optionally select specific modules to include
5. Enter an output prefix for the report file name
6. Click "Generate Flexible Grades Report" to create the report

### Technical Details

- All flexible reports are generated as Excel (.xlsx) files
- Reports are stored in the project's flexible_reports directory
- The generation process runs as a background task on the API server

## Setup Project Page

The Setup Project page allows users to create and validate project structures.

### Project Creation

This section allows you to create a new project with the proper folder structure.

#### Features

- Date input for the project (YY-MM-DD format)
- Class name input (optional, defaults to "CompITA Class")
- Current module selection
- Required files selection (gradebook, study_history, time_per_resource)
- Creation status display with real-time updates

#### Usage Instructions

1. Enter a project date in YY-MM-DD format
2. Optionally enter a class name
3. Select the current module number
4. Check the required files that will be included
5. Click "Create Project" to set up the project structure
6. Monitor the status display for progress updates

### Project Validation

This section allows you to validate an existing project structure.

#### Features

- Date input for the project to validate (YY-MM-DD format)
- Validation status display showing if the project is valid or invalid
- Detailed message explaining any issues found
- Project structure display showing the directory tree

#### Usage Instructions

1. Enter a project date in YY-MM-DD format
2. Click "Validate Project" to check the project structure
3. Review the validation status and message
4. If issues are found, address them and validate again

### Technical Details

- Project creation sets up the necessary directory structure for all CompITA reports
- The class_info.json file is created with the specified class name and current module
- Validation checks for required directories and files
- The directory structure is displayed as a text-based tree
