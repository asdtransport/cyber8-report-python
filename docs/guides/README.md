# CSV to JSON Parsers for Student Data

This project contains Python applications that parse CSV files containing student data and convert them to JSON format.

## Setup from Scratch

Follow these steps to set up and use this project from scratch:

### Prerequisites

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd report-python
   ```

2. **Create and activate a virtual environment:**

   Using `uv` (recommended):
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate  # On Windows
   ```

   Using standard Python tools:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**

   ```bash
   uv pip install pandas openpyxl tabulate matplotlib
   # OR
   pip install pandas openpyxl tabulate matplotlib
   ```

### Directory Structure Setup

Create the necessary directories for the project:

```bash
mkdir -p assets/comptia
mkdir -p assets/processed
mkdir -p reports
```

### Usage Workflow

1. **Place CSV files in the date-based input directory:**

   Create a date-based directory for your CSV files:
   ```bash
   mkdir -p assets/comptia/YY-MM-DD  # Replace YY-MM-DD with the current date (e.g., 25-04-29)
   ```

   Place your CSV files in this directory:
   - Class gradebook CSV: `assets/comptia/YY-MM-DD/classgradebook-*.csv`
   - Resource time CSV: `assets/comptia/YY-MM-DD/timeperresource-*.csv`
   - Study history CSV: `assets/comptia/YY-MM-DD/classstudyhistory-*.csv`

2. **Parse CSV files to JSON:**

   ```bash
   # Parse all file types from all date folders
   python csv_parser.py --all_dates --file_type classgradebook
   python csv_parser.py --all_dates --file_type timeperresource
   python csv_parser.py --all_dates --file_type studyhistory
   
   # OR parse files from a specific date
   python csv_parser.py --date YY-MM-DD --file_type classgradebook
   python csv_parser.py --date YY-MM-DD --file_type timeperresource
   python csv_parser.py --date YY-MM-DD --file_type studyhistory
   ```

3. **Generate reports:**

   ```bash
   # Generate all reports for the latest date
   python generate_reports.py --all
   
   # OR generate reports for a specific date
   python generate_reports.py --date YY-MM-DD --all
   ```

4. **View the generated reports:**

   The reports will be available in the `reports/YY-MM-DD/` directory:
   - Class summary: `class_report.csv` and `class_report.xlsx`
   - Module reports: `module_1_report.csv`, `module_2_report.csv`, etc.
   - Student reports: `student_Last_First_report.csv` for each student

### Automated Daily Reporting

For automated daily reporting, you can set up a cron job or scheduled task to run:

```bash
#!/bin/bash
cd /path/to/report-python
source .venv/bin/activate
python csv_parser.py --all_dates --file_type classgradebook
python csv_parser.py --all_dates --file_type timeperresource
python csv_parser.py --all_dates --file_type studyhistory
python generate_reports.py --all
```

Save this as `daily_report.sh`, make it executable with `chmod +x daily_report.sh`, and add it to your crontab.

### Teaching Assistant Tool

The project also includes a teaching assistant tool that provides interactive analysis and insights:

```bash
# Get insights for a specific student
python teaching_assistant.py --student "Last, First" --date YY-MM-DD

# List students at risk
python teaching_assistant.py --at-risk --date YY-MM-DD

# Analyze a specific module
python teaching_assistant.py --module 7 --date YY-MM-DD

# Generate visualizations
python teaching_assistant.py --visualize --date YY-MM-DD
```

## Installation

This project uses `uv` as the package manager. The virtual environment has already been set up with the required dependencies.

To activate the virtual environment:

```bash
source .venv/bin/activate
```

## Applications

### 1. Unified CSV Parser (`csv_parser.py`)

The unified CSV parser processes all types of CSV files (assessment data, resource time, and study history) and organizes output files in the `assets/processed/YY-MM-DD` directory structure. It supports continuous reports stored in date-based folders.

#### Usage

```bash
# Process the latest classgradebook CSV file
python3 csv_parser.py --file_type classgradebook

# Process the latest timeperresource CSV file
python3 csv_parser.py --file_type timeperresource

# Process the latest studyhistory CSV file
python3 csv_parser.py --file_type studyhistory

# Process a specific date's CSV files
python3 csv_parser.py --date 25-04-29 --file_type classgradebook
python3 csv_parser.py --date 25-04-29 --file_type timeperresource
python3 csv_parser.py --date 25-04-29 --file_type studyhistory

# Process all file types for the latest date
python3 csv_parser.py

# Process all file types for a specific date
python3 csv_parser.py --date 25-04-29

# Process a specific CSV file
python3 csv_parser.py --csv_file assets/comptia/25-04-29/classgradebook-4-29-8am.csv

# Process all date folders
python3 csv_parser.py --all_dates --file_type classgradebook
```

#### Command Line Options

| Option | Description |
|--------|-------------|
| `--csv_file` | Path to a specific CSV file (optional) |
| `--base_dir` | Base directory containing date folders (default: assets/comptia) |
| `--date` | Specific date folder to process (format: YY-MM-DD) |
| `--file_type` | Type of CSV file to process (classgradebook, timeperresource, studyhistory) |
| `--all_dates` | Process all date folders |
| `-o, --output` | Directory to save the JSON output (optional) |
| `--parser_type` | Type of parser to use (gradebook, resource, study) - legacy option |

#### File Types

The unified parser supports three file types, each with its own parsing logic and output format:

1. **classgradebook** - For class gradebook CSV files (student assessment data)
   ```bash
   python3 csv_parser.py --file_type classgradebook
   python3 csv_parser.py --date 25-04-29 --file_type classgradebook
   python3 csv_parser.py --all_dates --file_type classgradebook
   ```

2. **timeperresource** - For time per resource CSV files (time spent data)
   ```bash
   python3 csv_parser.py --file_type timeperresource
   python3 csv_parser.py --date 25-04-29 --file_type timeperresource
   python3 csv_parser.py --all_dates --file_type timeperresource
   ```

3. **studyhistory** - For class study history CSV files (daily study time data)
   ```bash
   python3 csv_parser.py --file_type studyhistory
   python3 csv_parser.py --date 25-04-29 --file_type studyhistory
   python3 csv_parser.py --all_dates --file_type studyhistory
   ```

#### Directory Structure

The parser expects CSV files to be organized in date-based folders:

```
assets/
└── comptia/
    ├── 25-04-28/
    │   ├── classgradebook-4-28-9pm.csv
    │   ├── timeperresource-04-28-9pm.csv
    │   └── classstudyhistory-04-28-9pm.csv
    └── 25-04-29/
        ├── classgradebook-4-29-8am.csv
        ├── timeperresource-04-29-8am.csv
        └── classstudyhistory-04-29-8am.csv
```

Output files are organized in a similar structure:

```
assets/
└── processed/
    ├── 25-04-28/
    │   ├── classgradebook-4-28-9pm.json
    │   ├── timeperresource-04-28-9pm.json
    │   └── classstudyhistory-04-28-9pm.json
    └── 25-04-29/
        ├── classgradebook-4-29-8am.json
        ├── timeperresource-04-29-8am.json
        └── classstudyhistory-04-29-8am.json
```

#### Examples

```bash
# Process the latest classgradebook CSV and save to assets/processed/YY-MM-DD/
python3 csv_parser.py --file_type classgradebook

# Process all CSV files from April 29, 2025
python3 csv_parser.py --date 25-04-29

# Process a specific CSV file and save to assets/processed/YY-MM-DD/
python3 csv_parser.py --csv_file assets/comptia/25-04-29/timeperresource-04-29-8am.csv
```

#### Output JSON Formats

##### 1. Class Gradebook (Assessment Data) JSON Format

```json
{
  "students": [
    {
      "name": "Student Name",
      "email": "student.email@example.com",
      "assessments": [...],
      "labs": [...],
      "lessons": [...],
      "fact_sheets": [...],
      "videos": [...],
      "other": [...],
      "summary": {
        "total_completed": 42,
        "total_items": 50,
        "completion_percentage": 0.84
      }
    }
  ],
  "metadata": {
    "total_students": 1,
    "assessment_types": {
      "assessment": 10,
      "lab": 5,
      "lesson": 15,
      "fact_sheet": 20,
      "video": 0,
      "other": 0
    }
  }
}
```

##### 2. Study History JSON Format

```json
{
  "students": [
    {
      "name": "Student Name",
      "email": "student.email@example.com",
      "total_study_time_seconds": 170991,
      "total_study_time_formatted": "47h 29m 51s",
      "daily_study": [
        {
          "date": "Apr 15, Tuesday",
          "study_time_seconds": 4417,
          "study_time_formatted": "1h 13m 37s"
        }
      ],
      "study_days": 14,
      "average_daily_study_time_seconds": 12213,
      "average_daily_study_time_formatted": "3h 23m 33s"
    }
  ],
  "metadata": {
    "total_students": 18,
    "date_range": {
      "start_date": "Apr 1, Tuesday",
      "end_date": "Jun 30, Monday"
    },
    "total_study_days": 91,
    "class_total_study_time_seconds": 1510528,
    "class_total_study_time_formatted": "419h 35m 28s",
    "class_average_study_time_seconds": 83918,
    "class_average_study_time_formatted": "23h 18m 38s"
  }
}
```

##### 3. Resource Time JSON Format

```json
{
  "students": [
    {
      "name": "Student Name",
      "email": "student.email@example.com",
      "resources": {
        "assessment": [
          {
            "name": "Assessment Name",
            "time_seconds": 1468,
            "time_formatted": "24m 28s"
          }
        ],
        "lab": [...],
        "fact_sheet": [...],
        "lesson": [...],
        "video": [...],
        "other": [...]
      },
      "summary": {
        "total_time_seconds": 12345,
        "total_time_formatted": "3h 25m 45s",
        "resource_type_summary": {
          "assessment": {
            "count": 10,
            "total_time_seconds": 3600,
            "total_time_formatted": "1h",
            "average_time_seconds": 360,
            "average_time_formatted": "6m"
          },
          "lab": {...},
          "fact_sheet": {...},
          "lesson": {...},
          "video": {...},
          "other": {...}
        }
      }
    }
  ],
  "metadata": {
    "total_students": 18,
    "resource_types": {
      "assessment": {
        "count": 25,
        "total_time_seconds": 36000,
        "total_time_formatted": "10h"
      },
      "lab": {...},
      "fact_sheet": {...},
      "lesson": {...},
      "video": {...},
      "other": {...}
    },
    "total_resources": 150,
    "class_total_time_seconds": 180000,
    "class_total_time_formatted": "50h"
  }
}
```

### 2. Report Generator (`generate_reports.py`)

Generates CSV reports from the JSON data produced by the parsers. It can generate reports for specific students, modules, or the entire class.

#### Updated Functionality

The report generator has been updated to work with the date-based directory structure:

- Automatically finds and uses JSON files from the `assets/processed/YY-MM-DD/` directory
- Organizes output reports in the `reports/YY-MM-DD/` directory structure
- Supports specifying a particular date folder to use via the `--date` parameter
- Automatically detects the latest date folder if no date is specified
- Can generate all reports (module, student, class, and Excel) with a single command using `--all`
- Properly separates labs from fact sheets in module reports for accurate completion tracking

#### Usage

```bash
# Generate all reports (module, student, class, and Excel) for the latest date
python3 generate_reports.py --all

# Generate all reports for a specific date
python3 generate_reports.py --date 25-04-29 --all

# Generate an Excel report for the latest date
python3 generate_reports.py --excel

# Generate a CSV report for a specific date
python3 generate_reports.py --date 25-04-29

# Generate a module-specific report
python3 generate_reports.py --date 25-04-29 --module 1

# Generate a student-specific report
python3 generate_reports.py --date 25-04-29 --student "Student Name"

# Generate a module-specific report for a specific student
python3 generate_reports.py --date 25-04-29 --module 1 --student "Student Name"

# Generate a report with a custom output path
python3 generate_reports.py --date 25-04-29 --output /path/to/custom/report.csv
```

#### Command Line Options

| Option | Description |
|--------|-------------|
| `--assessment-data` | Path to the assessment data JSON file (optional, auto-detected if not specified) |
| `--resource-time-data` | Path to the resource time data JSON file (optional, auto-detected if not specified) |
| `--output` | Path to save the CSV/Excel report (optional, auto-generated if not specified) |
| `--module` | Module number to generate the report for (optional) |
| `--student` | Student name to generate the report for (optional) |
| `--current-module` | Current module being taught (default: 7) |
| `--excel` | Generate an Excel report instead of a CSV report |
| `--date` | Date folder to use (format: YY-MM-DD, optional) |
| `--all` | Generate all reports: module reports, student reports, class report, and Excel report |

#### Report Types

The script can generate several types of reports:

1. **Class Report**: A summary of all students' progress, including completion percentages, time spent, and assessment scores.
2. **Module Reports**: Detailed reports for specific modules, showing each student's progress in that module.
3. **Student Reports**: Detailed reports for specific students, showing their progress across all modules.
4. **Excel Report**: A comprehensive Excel workbook with multiple sheets - one for each module plus a class summary.

#### Directory Structure

The report generator expects JSON files to be organized in date-based folders:

```
assets/
└── processed/
    ├── 25-04-28/
    │   ├── classgradebook-4-28-9pm.json
    │   ├── timeperresource-04-28-9pm.json
    │   └── classstudyhistory-04-28-9pm.json
    └── 25-04-29/
        ├── classgradebook-4-29-8am.json
        ├── timeperresource-04-29-8am.json
        └── classstudyhistory-04-29-8am.json
```

Output reports are organized in a similar structure:

```
reports/
├── 25-04-28/
│   ├── class_report.csv
│   ├── class_report.xlsx
│   ├── module_1_report.csv
│   ├── module_2_report.csv
│   └── student_John_Doe_report.csv
└── 25-04-29/
    ├── class_report.csv
    ├── class_report.xlsx
    ├── module_1_report.csv
    ├── module_2_report.csv
    └── student_John_Doe_report.csv
```

#### Generated Reports with --all

When using the `--all` flag, the script generates:

1. A class report CSV (`class_report.csv`)
2. Individual module reports for each module found in the data (`module_1_report.csv`, `module_2_report.csv`, etc.)
3. Individual student reports for each student (`student_John_Doe_report.csv`, etc.)
4. A comprehensive Excel report with multiple sheets (`class_report.xlsx`)

All reports are saved in the date-based directory structure (`reports/YY-MM-DD/`).

#### Examples

```bash
# Generate all reports for the latest date
python3 generate_reports.py --all

# Generate all reports for a specific date
python3 generate_reports.py --date 25-04-29 --all

# Generate a class report in Excel format for the latest date
python3 generate_reports.py --excel

# Generate a module report for module 3 from April 29, 2025
python3 generate_reports.py --date 25-04-29 --module 3

# Generate a student report for "John Doe" from April 29, 2025
python3 generate_reports.py --date 25-04-29 --student "John Doe"

# Generate an Excel report for module 2 from April 29, 2025
python3 generate_reports.py --date 25-04-29 --module 2 --excel

# Generate a report with a custom filename
python3 generate_reports.py --date 25-04-29 --output reports/custom_report.csv
```

#### Automated Daily Reporting

For automated daily reporting, you can set up a cron job or scheduled task to run:

```bash
python3 csv_parser.py --all_dates --file_type classgradebook
python3 csv_parser.py --all_dates --file_type timeperresource
python3 csv_parser.py --all_dates --file_type studyhistory
python3 generate_reports.py --all
```

This will process all CSV files and generate all reports for the latest date.

## Assessment Types

The assessment parser categorizes each column in the CSV file into one of the following types:
- `assessment`: Columns containing "Assessment" in their name
- `lab`: Columns containing "Lab" in their name
- `lesson`: Columns containing "Lesson" in their name
- `fact_sheet`: Columns containing "Fact Sheet" in their name
- `video`: Columns containing "Video" in their name
- `other`: Any other columns that don't match the above categories
