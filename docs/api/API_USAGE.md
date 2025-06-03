# CompITA Report Generator API

The CompITA Report Generator now includes a powerful API and web interface that allows you to generate reports, parse CSV files, and access metrics through a RESTful API and user-friendly web interface.

## API Features

- **RESTful API**: Access all CompITA Report Generator functionality through a modern REST API
- **Background Tasks**: All report generation happens in the background with status tracking
- **File Upload**: Upload CSV files directly through the API
- **Report Downloads**: Download generated reports in various formats
- **Comprehensive Documentation**: Auto-generated API documentation with Swagger UI

## Web Interface Features

- **User-Friendly Interface**: Modern, responsive web interface for easy interaction
- **Report Generation**: Generate reports with a few clicks
- **File Upload**: Upload CSV files through the web interface
- **Report Viewing**: View and download generated reports
- **Task Status Tracking**: Track the status of background tasks

## Using the API and Web Interface

### Starting the API Server

```bash
# Start the API server
compita api --host 0.0.0.0 --port 8000

# Start with auto-reload for development
compita api --reload
```

The API server will start and be accessible at http://localhost:8000. API documentation is available at http://localhost:8000/docs.

### Starting the Web Interface

```bash
# Start the web interface
compita web --host 0.0.0.0 --port 8080

# Connect to a custom API URL
compita web --api-url http://api-server:8000
```

The web interface will start and be accessible at http://localhost:8080.

### Starting Both API and Web Interface

```bash
# Start both API and web interface with one command
compita app

# Customize ports
compita app --api-port 8000 --web-port 8080

# Enable auto-reload for development
compita app --reload
```

This will start both the API server and web interface, with the web interface automatically configured to connect to the API.

## API Endpoints

The API provides the following endpoints:

- `/api/v1/parse-csv`: Parse CSV files to JSON
- `/api/v1/collect-metrics`: Collect and combine metrics from all data sources
- `/api/v1/flexible-module`: Generate flexible module report
- `/api/v1/flexible-assessment`: Generate flexible assessment report
- `/api/v1/flexible-grades`: Generate flexible grades report
- `/api/v1/student-reports`: Generate student reports
- `/api/v1/class-summary`: Generate class summary report
- `/api/v1/markdown-to-pdf`: Convert markdown to PDF
- `/api/v1/upload-csv`: Upload and parse a CSV file
- `/api/v1/generate-all`: Generate all reports for a specific date
- `/api/v1/available-dates`: Get a list of available date folders
- `/api/v1/download-report/{date}/{report_type}/{filename}`: Download a generated report file
- `/api/v1/status/{task_id}`: Get the status of a background task

## Web Interface Sections

The web interface provides the following sections:

1. **Generate Reports**: Generate all reports for a specific date
2. **Upload CSV Files**: Upload and parse CSV files
3. **Available Reports**: View and download generated reports

## Installation

The API and web interface are included in the standard CompITA Report Generator installation. If you're using the standalone executable, all dependencies are already bundled.

If you're installing from source, you'll need to install the additional dependencies:

```bash
# Using uv (recommended)
uv pip install -e ".[api]"

# Using pip
pip install -e ".[api]"
```

## Development

For development, you can use the auto-reload feature to automatically reload the API server when code changes:

```bash
compita api --reload
```

The web interface files are located in the `compita/src/web` directory. You can modify these files to customize the web interface.

## Troubleshooting

### API Server Won't Start

If the API server won't start, check that you have installed the required dependencies:

```bash
uv pip install fastapi uvicorn python-multipart
```

### Web Interface Can't Connect to API

If the web interface can't connect to the API, check that:

1. The API server is running
2. The API URL is correct (default: http://localhost:8000)
3. There are no network restrictions blocking the connection

You can specify a custom API URL when starting the web interface:

```bash
compita web --api-url http://api-server:8000
```

### Command Not Found

If you get a "command not found" error, make sure that:

1. You have installed the CompITA Report Generator
2. The installation directory is in your PATH
3. You are using the correct command name

If you're using the standalone executable, make sure it's properly installed in your `~/bin` directory and that directory is in your PATH.
