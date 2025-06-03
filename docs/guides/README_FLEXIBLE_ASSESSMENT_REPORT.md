# Flexible Assessment Report Generator

This tool generates customizable reports for student study time data, allowing you to analyze student progress across any date range.

## Features

- **Flexible Date Range Selection**: Analyze study time over any arbitrary date range
- **Subset Comparison**: Compare overall progress with a specific subset date range
- **Custom Output Naming**: Name your reports based on their content or purpose
- **Multi-format Output**: Generate both CSV and Excel reports
- **Weekly Breakdown Sheets**: Excel reports include separate sheets for each week
- **Configuration Documentation**: Reports include details about which date ranges were included
- **Study Threshold Support**: Option to set minimum study time to count a day as a study day
- **Standardized Naming**: Reports include timestamps for easy identification

## Installation

The Flexible Assessment Report Generator requires the following dependencies:
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
python flexible_assessment_report.py --date YY-MM-DD
```

This will generate a report for the default date range (Apr 15 to May 5) for the specified date folder.

### Command Line Options

| Option | Description |
|--------|-------------|
| `--date` | Specific date folder to process (format: YY-MM-DD) [required] |
| `--date-range` | Date range for overall analysis (format: "MMM D MMM D", e.g., "Apr 15 May 5") [default: "Apr 15 May 5"] |
| `--subset-range` | Date range for subset analysis (format: "MMM D MMM D", e.g., "Apr 15 Apr 30") [optional] |
| `--output-prefix` | Prefix for the output files (default: standardized name with timestamp) |
| `--min-study-threshold` | Minimum study time in seconds to count a day as a study day (default: 0) |

### Examples

#### Custom date range

```bash
python flexible_assessment_report.py --date 25-05-05 --date-range "Apr 1 May 15"
```

This will generate a report analyzing study time from April 1 to May 15.

#### With subset comparison

```bash
python flexible_assessment_report.py --date 25-05-05 --date-range "Apr 1 May 15" --subset-range "Apr 15 Apr 30"
```

This will generate a report analyzing study time from April 1 to May 15, with a subset comparison of April 15 to April 30.

#### Custom output filename

```bash
python flexible_assessment_report.py --date 25-05-05 --output-prefix early_assessments
```

This will generate a report with a custom filename prefix.

#### Set minimum study threshold

```bash
python flexible_assessment_report.py --date 25-05-05 --min-study-threshold 300
```

This will only count days with at least 5 minutes (300 seconds) of study time as study days, providing a more meaningful assessment of student engagement.

## Output

The script generates two output files in the `reports/YY-MM-DD/assessment_reports/` directory:

1. **CSV Report**: `{output_prefix}.csv`
   - Contains the summary data for all students
   - Includes total study time, study days, and average daily study time

2. **Excel Report**: `{output_prefix}.xlsx`
   - Contains multiple sheets:
     - **Summary**: Overall student performance data
     - **Week X**: Individual sheets for each week showing daily study time
     - **Configuration**: Details about which date ranges were included and how the report was generated

3. **Standardized Copy**: `assessment_report_YY-MM-DD_Month-DD-YYYY_at_HH-MM-AM/PM.xlsx`
   - A copy of the Excel report with a standardized naming convention
   - Includes a human-readable timestamp for easy identification
   - Created automatically when a custom output prefix is used

## Data Source

The report generator uses data from the processed JSON files in the `assets/processed/YY-MM-DD/` directory. Specifically, it uses the `classstudyhistory-*.json` file to extract study time data for each student.

## Understanding the Report

### Main Summary Sheet

The main summary sheet in the Excel report includes the following columns:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Total Study Time (Range)**: Total study time across the specified date range
- **Study Days (Range)**: Number of days with study activity in the date range
- **Avg. Daily Study Time (Range)**: Average study time per study day
- **Total Study Time (Subset)**: Total study time across the subset date range
- **Study Days (Subset)**: Number of days with study activity in the subset range
- **Avg. Daily Study Time (Subset)**: Average study time per study day in the subset

### Weekly Breakdown Sheets

Each week has its own sheet in the Excel report, showing:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **[Date]**: Study time for each date in the week
- **Week Total**: Total study time for the week

All students are included in each week sheet, even if they have no study time for that week.

## Integration with Other Tools

The Flexible Assessment Report Generator is designed to work with the other tools in the CompTIA reporting system:

1. First, process the raw CSV files:
   ```bash
   python csv_parser.py --date YY-MM-DD
   ```

2. Generate the basic reports:
   ```bash
   python generate_reports.py --date YY-MM-DD --all
   ```

3. Generate the flexible assessment report:
   ```bash
   python flexible_assessment_report.py --date YY-MM-DD [options]
   ```

## Troubleshooting

If you encounter any issues with the report generator:

1. **Missing data**: Ensure that the CSV parser has been run for the specified date
2. **No study history found**: Check that the classstudyhistory JSON file exists in the processed directory
3. **Empty reports**: Verify that the date range specified contains study activity

## Limitations

- The report generator only works with data that has been processed by the CSV parser
- Date formats must follow the pattern "MMM D" (e.g., "Apr 15")
- The script assumes that date strings in the study history follow the pattern "MMM D, Day" (e.g., "Apr 15, Tuesday")

## Future Enhancements

Potential future enhancements to the report generator include:

- Support for custom day-of-week filtering (e.g., weekdays only)
- Additional statistical analysis
- Student grouping and filtering options
- Graphical visualizations of study patterns
- Correlation analysis with module completion data
