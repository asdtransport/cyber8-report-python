# CompITA Report Generator API

This document provides an overview of the CompITA Report Generator API.

## Package Structure

The CompITA Report Generator is organized into several modules:

- `compita.parsers`: Modules for parsing CSV and JSON data
- `compita.collectors`: Modules for collecting and processing metrics
- `compita.reports`: Modules for generating various report types
- `compita.converters`: Modules for converting between different formats
- `compita.utils`: Utility modules used across the package
- `compita.cli`: Command-line interface modules

## Parsers API

### CSV Parser

```python
from compita.parsers.csv_parser import parse_csv

# Parse a CSV file
parse_csv(date='25-05-05', file_type='classgradebook', parser_type='gradebook')
```

### Parser Utilities

```python
from compita.parsers.utils import find_latest_date_folder, find_csv_files

# Find the latest date folder
latest_folder = find_latest_date_folder('assets/comptia')

# Find CSV files of a specific type
csv_files = find_csv_files('assets/comptia/25-05-05', 'classgradebook')
```

## Collectors API

### Metrics Collector

```python
from compita.collectors.metrics_collector import collect_metrics

# Collect metrics for a specific date
collect_metrics(date='25-05-05')
```

### Collector Utilities

```python
from compita.collectors.utils import load_json_data, save_json_data, get_week_number

# Load JSON data
data = load_json_data('path/to/file.json')

# Save JSON data
save_json_data(data, 'path/to/output.json')

# Get week number from a date string
week_num = get_week_number('Apr 20, 2025')
```

## Reports API

### Report Generator

```python
from compita.reports.report_generator import generate_reports, generate_class_summary

# Generate student reports
generate_reports(date='25-05-05')

# Generate class summary report
generate_class_summary(date='25-05-05')
```

### Flexible Reports

```python
from compita.reports.flexible_module import generate_flexible_module_report
from compita.reports.flexible_assessment import generate_flexible_assessment_report
from compita.reports.flexible_grades import generate_flexible_grades_report

# Generate flexible module report
generate_flexible_module_report(
    date='25-05-05',
    all_modules=['1', '2', '3'],
    subset_modules=['2', '3'],
    exclude_modules=['4'],
    output_prefix='custom_prefix',
    count_partial=True
)

# Generate flexible assessment report
generate_flexible_assessment_report(
    date='25-05-05',
    date_range='Apr 15 May 5',
    subset_range='Apr 15 Apr 30',
    output_prefix='custom_prefix',
    min_study_threshold=300
)

# Generate flexible grades report
generate_flexible_grades_report(
    date='25-05-05',
    all_modules=['1', '2', '3'],
    subset_modules=['2', '3'],
    exclude_modules=['4'],
    assessment_types=['Module Quiz', 'Lesson Review'],
    output_prefix='custom_prefix',
    min_grade_threshold=0.8,
    count_incomplete=False
)
```

### Report Formatter

```python
from compita.reports.report_formatter import format_student_report, format_class_summary

# Format a student report
markdown_content = format_student_report(student_data, date='25-05-05')

# Format a class summary report
markdown_content = format_class_summary(class_data, date='25-05-05')
```

## Converters API

### Markdown to PDF Converter

```python
from compita.converters.markdown_to_pdf import convert_markdown_to_pdf

# Convert markdown files to PDF
convert_markdown_to_pdf(
    input_dir='reports/25-05-05/progress_reports/student_reports',
    output_dir='reports/25-05-05/executive_reports'
)
```

### Converter Utilities

```python
from compita.converters.utils import extract_title_from_markdown, get_css_for_report_type

# Extract title from markdown content
title = extract_title_from_markdown(markdown_content)

# Get CSS for a specific report type
css = get_css_for_report_type('student')
```

## Utilities API

### Configuration

```python
from compita.utils.config import config

# Get paths
processed_data_path = config.get_processed_data_path('25-05-05', 'gradebook')
reports_path = config.get_reports_path('25-05-05', 'progress')

# Ensure directories exist
config.ensure_directories('25-05-05')
```

### Logging

```python
from compita.utils.logger import setup_logger

# Set up a logger
logger = setup_logger('my_module')
logger.info('This is an info message')
logger.error('This is an error message')
```

### Helper Functions

```python
from compita.utils.helpers import format_time_seconds, ensure_directory

# Format seconds to a human-readable string
formatted_time = format_time_seconds(3665)  # "1h 1m 5s"

# Ensure a directory exists
path = ensure_directory('path/to/directory')
```

## CLI API

### Command Line Interface

```bash
# Generate all reports
compita-generate-all --date 25-05-05

# Generate flexible module report
compita-flexible-module --date 25-05-05 --all-modules 1 2 3 4

# Generate flexible assessment report
compita-flexible-assessment --date 25-05-05 --date-range "Apr 15 May 5"

# Generate flexible grades report
compita-flexible-grades --date 25-05-05 --min-grade-threshold 0.8

# Convert markdown to PDF
compita-markdown-to-pdf --input-dir reports/25-05-05/progress_reports/student_reports --output-dir reports/25-05-05/executive_reports
```

### Programmatic CLI Usage

```python
from compita.cli.commands import run_command
import sys

# Set up arguments
sys.argv = ['compita-cli', 'generate-all', '--date', '25-05-05']

# Run the command
exit_code = run_command()
```
