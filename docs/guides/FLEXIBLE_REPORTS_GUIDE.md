# Flexible Reports Guide

This guide explains how to use the three flexible report generators in the CompITA Report Generator package.

## Overview

The CompITA Report Generator includes three specialized flexible report generators:

1. **Flexible Module Report**: Analyzes module completion percentages
2. **Flexible Assessment Report**: Analyzes student study time data
3. **Flexible Grades Report**: Analyzes assessment grades

These flexible reports provide more detailed analysis than the standard reports and allow for customized filtering and analysis of student data.

## Flexible Module Report

The Flexible Module Report analyzes module completion percentages for students.

### Basic Usage

```bash
# Using the CLI
compita-flexible-module --date 25-05-05

# Using the Python API
from compita.reports.flexible_module import generate_flexible_module_report
generate_flexible_module_report(date='25-05-05')
```

### Options

- `--all-modules`: List of module numbers to include in the overall analysis (default: 1-14)
- `--subset-modules`: List of module numbers to include in the subset analysis (default: 6-8)
- `--exclude-modules`: List of module numbers to exclude from the overall analysis
- `--output-prefix`: Prefix for the output files (default: "module_report")
- `--count-partial`: Count partial completions as fully completed

### Examples

```bash
# Custom module selection
compita-flexible-module --date 25-05-05 --all-modules 1 2 4 5 --subset-modules 4 5

# Exclude specific modules
compita-flexible-module --date 25-05-05 --exclude-modules 3

# Count partial completions as fully completed
compita-flexible-module --date 25-05-05 --count-partial
```

### Output

The Flexible Module Report generates:
- CSV report: `reports/25-05-05/progress_reports/progress_report_*.csv`
- Excel report: `reports/25-05-05/progress_reports/progress_report_*.xlsx`

## Flexible Assessment Report

The Flexible Assessment Report analyzes student study time data.

### Basic Usage

```bash
# Using the CLI
compita-flexible-assessment --date 25-05-05

# Using the Python API
from compita.reports.flexible_assessment import generate_flexible_assessment_report
generate_flexible_assessment_report(date='25-05-05')
```

### Options

- `--date-range`: Date range for overall analysis (format: "MMM D MMM D", e.g., "Apr 15 May 5")
- `--subset-range`: Date range for subset analysis (format: "MMM D MMM D", e.g., "Apr 15 Apr 30")
- `--output-prefix`: Prefix for the output files (default: "assessment_report")
- `--min-study-threshold`: Minimum study time in seconds to count a day as a study day (default: 60)

### Examples

```bash
# Custom date ranges
compita-flexible-assessment --date 25-05-05 --date-range "Apr 15 May 5" --subset-range "Apr 15 Apr 30"

# Set minimum study threshold
compita-flexible-assessment --date 25-05-05 --min-study-threshold 300
```

### Output

The Flexible Assessment Report generates:
- CSV report: `reports/25-05-05/assessment_reports/assessment_report_*.csv`
- Excel report: `reports/25-05-05/assessment_reports/assessment_report_*.xlsx`

## Flexible Grades Report

The Flexible Grades Report analyzes assessment grades for students.

### Basic Usage

```bash
# Using the CLI
compita-flexible-grades --date 25-05-05

# Using the Python API
from compita.reports.flexible_grades import generate_flexible_grades_report
generate_flexible_grades_report(date='25-05-05')
```

### Options

- `--all-modules`: List of module numbers to include in the overall analysis (default: 1-14)
- `--subset-modules`: List of module numbers to include in the subset analysis (default: 6-8)
- `--exclude-modules`: List of module numbers to exclude from the analysis
- `--assessment-types`: List of assessment types to include (e.g., "Module Quiz" "Lesson Review" "Interactive")
- `--output-prefix`: Prefix for the output files (default: "grades_report")
- `--min-grade-threshold`: Minimum grade (0.0-1.0) to count an assessment as passed (default: 0.7)
- `--count-incomplete`: Count assessments with 0.0 completion in averages

### Examples

```bash
# Custom module selection and assessment types
compita-flexible-grades --date 25-05-05 --all-modules 1 2 3 --assessment-types "Module Quiz" "Lesson Review"

# Set minimum grade threshold
compita-flexible-grades --date 25-05-05 --min-grade-threshold 0.8
```

### Output

The Flexible Grades Report generates:
- CSV report: `reports/25-05-05/grades_reports/grades_report_*.csv`
- Excel report: `reports/25-05-05/grades_reports/grades_report_*.xlsx`

## Integrating Flexible Reports into the Workflow

The flexible reports are typically generated after parsing the CSV files to JSON and before generating the standard reports:

```bash
# Complete workflow
# 1. Parse CSV files to JSON
python -m compita.parsers.csv_parser --date 25-05-05 --file_type classgradebook --parser_type gradebook
python -m compita.parsers.csv_parser --date 25-05-05 --file_type studyhistory --parser_type study
python -m compita.parsers.csv_parser --date 25-05-05 --file_type timeperresource --parser_type resource

# 2. Generate flexible reports
python -m compita.reports.flexible_module --date 25-05-05
python -m compita.reports.flexible_assessment --date 25-05-05
python -m compita.reports.flexible_grades --date 25-05-05

# 3. Continue with the rest of the workflow
# ...
```

Alternatively, you can use the `compita-generate-all` command to run the entire workflow, including the flexible reports:

```bash
compita-generate-all --date 25-05-05
```

## Analyzing the Reports

The flexible reports provide detailed analysis of student performance in different areas:

1. **Module Completion**: The Flexible Module Report shows which students have completed which modules and allows you to focus on specific module subsets.

2. **Study Time**: The Flexible Assessment Report analyzes how much time students spend studying, which days they study, and allows you to focus on specific date ranges.

3. **Assessment Grades**: The Flexible Grades Report analyzes student grades on different types of assessments and allows you to focus on specific module subsets and assessment types.

These reports are useful for identifying students who may need additional support, recognizing high-performing students, and understanding overall class performance.
