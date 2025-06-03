# Flexible Grades Report Generator

This tool generates customizable reports for student assessment grades, allowing you to analyze student performance across any combination of modules and assessment types.

## Features

- **Flexible Module Selection**: Analyze any arbitrary set of modules' assessments
- **Subset Comparison**: Compare overall performance with a specific subset of modules
- **Module Exclusion**: Easily exclude specific modules from the analysis
- **Assessment Type Filtering**: Focus on specific assessment types (e.g., Module Quiz, Lesson Review, Interactive)
- **Custom Output Naming**: Name your reports based on their content or purpose
- **Multi-format Output**: Generate both CSV and Excel reports
- **Module-specific Sheets**: Excel reports include separate sheets for each module
- **Assessment Type Sheets**: Excel reports include separate sheets for each assessment type
- **Detailed Assessment View**: Complete breakdown of all individual assessment scores
- **Configuration Documentation**: Reports include details about which modules and assessment types were included
- **Minimum Grade Threshold**: Set a custom passing threshold for assessments
- **Standardized Naming**: Reports include timestamps for easy identification

## Installation

The Flexible Grades Report Generator requires the following dependencies:
- Python 3.8+
- pandas
- openpyxl

These dependencies should already be installed if you've set up the main project:

```bash
uv pip install pandas openpyxl
```

## Usage

### Basic Usage

```bash
python flexible_grades_report.py --date YY-MM-DD
```

This will generate a report for modules 1-14 (overall) and modules 6-8 (subset) for the specified date, with a default passing threshold of 70%.

### Command Line Options

| Option | Description |
|--------|-------------|
| `--date` | Specific date folder to process (format: YY-MM-DD) [required] |
| `--all-modules` | List of module numbers to include in the overall analysis (default: 1-14) |
| `--subset-modules` | List of module numbers to include in the subset analysis (default: 6-8) |
| `--exclude-modules` | List of module numbers to exclude from the analysis |
| `--assessment-types` | List of assessment types to include (e.g., "Module Quiz" "Lesson Review" "Interactive") |
| `--output-prefix` | Prefix for the output files (default: standardized name with timestamp) |
| `--min-grade-threshold` | Minimum grade (0.0-1.0) to count an assessment as passed (default: 0.7) |
| `--count-incomplete` | Count assessments with 0.0 completion in averages (flag, no value needed) |

### Examples

#### Exclude specific modules

```bash
python flexible_grades_report.py --date 25-05-05 --exclude-modules 3
```

This will generate a report for modules 1-2-4-5-6-7-8-9-10-11-12-13-14 (excluding module 3) and compare with modules 6-8.

#### Custom module selection

```bash
python flexible_grades_report.py --date 25-05-05 --all-modules 1 2 4 5 --subset-modules 4 5
```

This will generate a report focusing only on modules 1, 2, 4, and 5, with a subset comparison of modules 4 and 5.

#### Filter by assessment types

```bash
python flexible_grades_report.py --date 25-05-05 --assessment-types "Module Quiz" "Lesson Review"
```

This will generate a report that only includes Module Quiz and Lesson Review assessments, excluding other types like Interactive assessments.

#### Topic-specific analysis

```bash
python flexible_grades_report.py --date 25-05-05 --all-modules 3 6 9 12 --subset-modules 9 12 --output-prefix networking_grades
```

This will generate a report focusing on specific modules (e.g., networking-related modules) and save it with a descriptive prefix.

#### Custom passing threshold

```bash
python flexible_grades_report.py --date 25-05-05 --min-grade-threshold 0.8
```

This will set the passing threshold to 80% instead of the default 70%, providing a more stringent assessment of student performance.

#### Include incomplete assessments

```bash
python flexible_grades_report.py --date 25-05-05 --count-incomplete
```

This will include assessments with 0.0 completion in the average calculations, providing a more comprehensive view of student engagement with all assigned assessments.

## Output

The script generates two output files in the `reports/YY-MM-DD/grades_reports/` directory:

1. **CSV Report**: `{output_prefix}.csv`
   - Contains the summary data for all students
   - Includes average scores, completion percentages, and assessment counts

2. **Excel Report**: `{output_prefix}.xlsx`
   - Contains multiple sheets:
     - **Summary**: Overall student performance data
     - **Module X**: Individual sheets for each module showing student performance
     - **Assessment Type**: Sheets for each assessment type (e.g., Module Quiz, Lesson Review)
     - **Detailed Assessments**: Complete breakdown of all individual assessment scores
     - **Configuration**: Details about which modules and assessment types were included

3. **Standardized Copy**: `grades_report_YY-MM-DD_Month-DD-YYYY_at_HH-MM-AM/PM.xlsx`
   - A copy of the Excel report with a standardized naming convention
   - Includes a human-readable timestamp for easy identification
   - Created automatically when a custom output prefix is used

## Data Source

The report generator uses data from the processed JSON files in the `assets/processed/YY-MM-DD/` directory. Specifically, it uses the `classgradebook-*.json` file to extract assessment data for each student.

## Understanding the Report

### Main Summary Sheet

The main summary sheet in the Excel report includes the following columns:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Modules X-Y-Z Avg. Score**: Average score across all specified modules
- **Modules X-Y-Z Completion %**: Percentage of assessments passed (above threshold)
- **Modules X-Y-Z Assessments Completed**: Number of assessments passed
- **Modules X-Y-Z Total Assessments**: Total number of assessments
- **Modules A-B-C Avg. Score**: Average score across the subset modules
- **Modules A-B-C Completion %**: Percentage of assessments passed in the subset
- **Modules A-B-C Assessments Completed**: Number of assessments passed in the subset
- **Modules A-B-C Total Assessments**: Total number of assessments in the subset

### Module-specific Sheets

Each module has its own sheet in the Excel report, showing:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Module X Avg. Score**: Average score for this module
- **Module X Completion %**: Percentage of assessments passed for this module
- **Assessments Completed**: Number of assessments passed for this module
- **Total Assessments**: Total number of assessments in this module

### Assessment Type Sheets

Each assessment type has its own sheet in the Excel report, showing:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Assessment Type Avg. Score**: Average score for this assessment type
- **Assessment Type Completion %**: Percentage of assessments passed for this type
- **Assessments Completed**: Number of assessments passed for this type
- **Total Assessments**: Total number of assessments of this type

### Detailed Assessments Sheet

The detailed assessments sheet provides a complete breakdown of all individual assessment scores:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Module**: Module number
- **Assessment**: Full assessment name
- **Type**: Assessment type
- **Score**: Raw score (0.0-1.0)
- **Passed**: Whether the assessment was passed based on the threshold

## Integration with Other Tools

The Flexible Grades Report Generator is designed to work with the other tools in the CompTIA reporting system:

1. First, process the raw CSV files:
   ```bash
   python csv_parser.py --date YY-MM-DD
   ```

2. Generate the basic module reports:
   ```bash
   python generate_reports.py --date YY-MM-DD --all
   ```

3. Generate the flexible grades report:
   ```bash
   python flexible_grades_report.py --date YY-MM-DD [options]
   ```

## Troubleshooting

If you encounter any issues with the report generator:

1. **Missing data**: Ensure that the CSV parser has been run for the specified date
2. **No assessments found**: Check that the classgradebook JSON file exists in the processed directory
3. **Empty reports**: Verify that the modules specified actually contain assessments
4. **Assessment type filtering issues**: Check the exact spelling and capitalization of assessment types

## Limitations

- The report generator only works with data that has been processed by the CSV parser
- Module numbers must be integers between 1 and 14
- The script assumes that assessment names follow the pattern "Assessment - X.Y.Z Type" where X is the module number

## Future Enhancements

Potential future enhancements to the report generator include:

- Support for custom date ranges
- Additional statistical analysis
- Student grouping and filtering options
- Graphical visualizations of student performance
- Correlation analysis with study time data
- Trend analysis for multiple assessment points
