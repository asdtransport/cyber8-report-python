# CompITA Report Generator API Endpoints

This document provides detailed information about all available API endpoints in the CompITA Report Generator.

## Table of Contents

1. [Base URL](#base-url)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [API Endpoints](#api-endpoints)
   - [Core Endpoints](#core-endpoints)
   - [Report Generation Endpoints](#report-generation-endpoints)
   - [CSV Parsing Endpoints](#csv-parsing-endpoints)
   - [Project Management Endpoints](#project-management-endpoints)
   - [Dashboard Endpoints](#dashboard-endpoints)
6. [Background Tasks](#background-tasks)
7. [File Uploads](#file-uploads)
8. [Examples](#examples)

## Base URL

All API endpoints are relative to the base URL of the API server. By default, this is:

```
http://localhost:8000/api/v1
```

You can configure a different host or port when starting the API server:

```bash
compita api --host 127.0.0.1 --port 9000
```

## Authentication

The current version of the API does not require authentication. It is designed for local use or within a trusted network.

## Response Format

All API responses are in JSON format. Successful responses typically include:

- For immediate operations: The requested data or a success message
- For background tasks: A task ID and initial status information

Example success response:
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued successfully"
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes and a JSON response containing error details:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## API Endpoints

### Core Endpoints

#### `GET /`

Returns basic information about the API.

**Response:**
```json
{
  "name": "CompITA Report Generator API",
  "version": "1.0.0",
  "description": "API for generating student and class reports from CompITA data"
}
```

#### `GET /task/{task_id}`

Get the status of a background task.

**Parameters:**
- `task_id` (path): ID of the task to check

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "running",
  "message": "Generating reports...",
  "result": null
}
```

Status values can be:
- `queued`: Task is waiting to be processed
- `running`: Task is currently running
- `completed`: Task has completed successfully
- `failed`: Task has failed

### Report Generation Endpoints

#### `POST /generate-all`

Generate all reports for a specific date.

**Request Body:**
```json
{
  "date": "25-05-27"
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to generate all reports for 25-05-27"
}
```

#### `POST /flexible-module`

Generate a flexible module report.

**Request Body:**
```json
{
  "date": "25-05-27",
  "all_modules": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
  "subset_modules": [1, 2, 3],
  "exclude_modules": [10, 11],
  "output_prefix": "custom_module_report",
  "count_partial": true
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to generate flexible module report for 25-05-27"
}
```

#### `POST /flexible-assessment`

Generate a flexible assessment report.

**Request Body:**
```json
{
  "date": "25-05-27",
  "assessment_types": ["quiz", "exam", "assignment"],
  "output_prefix": "custom_assessment_report",
  "modules": [1, 2, 3, 4]
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to generate flexible assessment report for 25-05-27"
}
```

#### `POST /flexible-grades`

Generate a flexible grades report.

**Request Body:**
```json
{
  "date": "25-05-27",
  "grade_categories": ["quiz", "exam", "assignment"],
  "grade_weights": {"quiz": 0.3, "exam": 0.5, "assignment": 0.2},
  "output_prefix": "custom_grades_report",
  "modules": [1, 2, 3, 4]
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to generate flexible grades report for 25-05-27"
}
```

#### `POST /student-reports`

Generate student reports.

**Request Body:**
```json
{
  "date": "25-05-27",
  "students": ["student1", "student2"],
  "output_dir": "custom_output_dir",
  "assets_dir": "assets"
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to generate student reports for 25-05-27"
}
```

#### `POST /class-summary`

Generate a class summary report.

**Request Body:**
```json
{
  "date": "25-05-27",
  "output_dir": "custom_output_dir",
  "assets_dir": "assets"
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to generate class summary for 25-05-27"
}
```

#### `POST /markdown-to-pdf`

Convert markdown files to PDF.

**Request Body:**
```json
{
  "input_dir": "reports/25-05-27/markdown",
  "output_dir": "reports/25-05-27/pdf"
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to convert markdown to PDF"
}
```

### CSV Parsing Endpoints

#### `POST /parse-csv`

Parse CSV files to JSON.

**Request Body:**
```json
{
  "date": "25-05-27",
  "file_type": "assessment",
  "parser_type": "standard",
  "assets_dir": "assets"
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to parse CSV files for 25-05-27"
}
```

#### `POST /upload-csv`

Upload and parse a CSV file.

**Form Data:**
- `file`: The CSV file to upload
- `date`: Date in YY-MM-DD format
- `file_type`: Type of file (assessment, resource_time, etc.)
- `parser_type`: Type of parser to use (standard, custom)
- `assets_dir`: Assets directory (optional)

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to upload and parse CSV file"
}
```

#### `POST /collect-metrics`

Collect and combine metrics from all data sources.

**Request Body:**
```json
{
  "date": "25-05-27"
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to collect metrics for 25-05-27"
}
```

### Project Management Endpoints

#### `POST /setup-project`

Setup a new project with the proper folder structure.

**Request Body:**
```json
{
  "date": "25-05-27",
  "class_name": "CompITA Class",
  "current_module": 7,
  "required_files": ["gradebook", "study_history", "time_per_resource"]
}
```

**Response:**
```json
{
  "task_id": "12345678-1234-5678-1234-567812345678",
  "status": "queued",
  "message": "Task queued to setup project for 25-05-27"
}
```

#### `GET /validate-project/{date}`

Validate an existing project structure.

**Parameters:**
- `date` (path): Date in YY-MM-DD format

**Response:**
```json
{
  "valid": true,
  "message": "Project structure is valid",
  "structure": "assets/25-05-27/\n├── class_info.json\n├── processed/\n├── raw/\n└── students/"
}
```

#### `GET /available-dates`

Get a list of available date folders.

**Parameters:**
- `assets_dir` (query): Assets directory (optional, default: "assets")

**Response:**
```json
[
  "25-05-20",
  "25-05-27"
]
```

#### `GET /available-reports/{date}`

Get a list of available reports for a specific date.

**Parameters:**
- `date` (path): Date in YY-MM-DD format

**Response:**
```json
[
  {
    "type": "student",
    "name": "student1_report.pdf",
    "path": "reports/25-05-27/student/student1_report.pdf",
    "size": 1024
  },
  {
    "type": "class",
    "name": "class_summary.pdf",
    "path": "reports/25-05-27/class/class_summary.pdf",
    "size": 2048
  }
]
```

#### `GET /download-report/{date}/{report_type}/{filename}`

Download a generated report file.

**Parameters:**
- `date` (path): Date in YY-MM-DD format
- `report_type` (path): Type of report (student, class, module, etc.)
- `filename` (path): Name of the report file

**Response:**
The requested file as a downloadable attachment.

### Dashboard Endpoints

#### `GET /projects`

Get a list of all projects (dates) with additional metadata.

**Response:**
```json
[
  {
    "date": "25-05-27",
    "created_at": "2025-05-27T00:00:00",
    "class_name": "CompITA Class",
    "current_module": 7,
    "student_count": 25
  },
  {
    "date": "25-05-20",
    "created_at": "2025-05-20T00:00:00",
    "class_name": "Another Class",
    "current_module": 6,
    "student_count": 20
  }
]
```

#### `GET /reports`

Get a list of all generated reports across all dates.

**Response:**
```json
[
  {
    "date": "25-05-27",
    "created_at": "2025-05-27T00:00:00",
    "type": "student",
    "name": "student1_report.pdf",
    "path": "reports/25-05-27/student/student1_report.pdf",
    "size": 1024
  },
  {
    "date": "25-05-20",
    "created_at": "2025-05-20T00:00:00",
    "type": "class",
    "name": "class_summary.pdf",
    "path": "reports/25-05-20/class/class_summary.pdf",
    "size": 2048
  }
]
```

#### `GET /health`

API health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-05-29T22:30:00.000Z"
}
```

#### `GET /storage`

Check storage status and available space.

**Response:**
```json
{
  "status": "ok",
  "assets_size_bytes": 1048576,
  "assets_size_mb": 1.0,
  "disk_total_gb": 500.0,
  "disk_used_gb": 250.0,
  "disk_free_gb": 250.0,
  "disk_usage_percent": 50.0
}
```

## Background Tasks

Many API endpoints initiate long-running operations that are executed as background tasks. These endpoints return a task ID that can be used to check the status of the operation.

To check the status of a task:

```
GET /task/{task_id}
```

The response will include:
- `task_id`: The ID of the task
- `status`: Current status (queued, running, completed, failed)
- `message`: A human-readable message describing the current state
- `result`: The result of the task (if completed)

## File Uploads

The API supports file uploads through the `/upload-csv` endpoint. Files should be uploaded using multipart/form-data format.

Example using curl:

```bash
curl -X POST "http://localhost:8000/api/v1/upload-csv" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/file.csv" \
  -F "date=25-05-27" \
  -F "file_type=assessment" \
  -F "parser_type=standard"
```

## Examples

### Generate All Reports

```bash
curl -X POST "http://localhost:8000/api/v1/generate-all" \
  -H "Content-Type: application/json" \
  -d '{"date": "25-05-27"}'
```

### Check Task Status

```bash
curl -X GET "http://localhost:8000/api/v1/task/12345678-1234-5678-1234-567812345678"
```

### Validate Project

```bash
curl -X GET "http://localhost:8000/api/v1/validate-project/25-05-27"
```

### Get Available Reports

```bash
curl -X GET "http://localhost:8000/api/v1/available-reports/25-05-27"
```
