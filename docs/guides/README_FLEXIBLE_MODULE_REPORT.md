# Flexible Module Report Generator

This tool generates customizable reports for student module completion data, allowing you to analyze student progress across any combination of modules.

## Features

- **Flexible Module Selection**: Analyze any arbitrary set of modules
- **Subset Comparison**: Compare overall progress with a specific subset of modules
- **Module Exclusion**: Easily exclude specific modules from the analysis
- **Custom Output Naming**: Name your reports based on their content or purpose
- **Multi-format Output**: Generate both CSV and Excel reports
- **Module-specific Sheets**: Excel reports include separate sheets for each module
- **Configuration Documentation**: Reports include details about which modules were included
- **Partial Completion Support**: Option to count partially completed labs as fully completed
- **Standardized Naming**: Reports include timestamps for easy identification

## Installation

The Flexible Module Report Generator requires the following dependencies:
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
python flexible_module_report.py --date YY-MM-DD
```

This will generate a report for modules 1-14 (overall) and modules 6-8 (subset) for the specified date.

### Command Line Options

| Option | Description |
|--------|-------------|
| `--date` | Specific date folder to process (format: YY-MM-DD) [required] |
| `--all-modules` | List of module numbers to include in the overall analysis (default: 1-14) |
| `--subset-modules` | List of module numbers to include in the subset analysis (default: 6-8) |
| `--exclude-modules` | List of module numbers to exclude from the overall analysis |
| `--output-prefix` | Prefix for the output files (default: standardized name with timestamp) |
| `--count-partial` | Count partial completions as fully completed labs (flag, no value needed) |

### Examples

#### Exclude specific modules

```bash
python flexible_module_report.py --date 25-05-05 --exclude-modules 3
```

This will generate a report for modules 1-2-4-5-6-7-8-9-10-11-12-13-14 (excluding module 3) and compare with modules 6-8.

#### Custom module selection

```bash
python flexible_module_report.py --date 25-05-05 --all-modules 1 2 4 5 --subset-modules 4 5
```

This will generate a report focusing only on modules 1, 2, 4, and 5, with a subset comparison of modules 4 and 5.

#### Topic-specific analysis

```bash
python flexible_module_report.py --date 25-05-05 --all-modules 3 6 9 12 --subset-modules 9 12 --output-prefix networking_modules
```

This will generate a report focusing on specific modules (e.g., networking-related modules) and save it with a descriptive prefix.

#### Early vs. Late modules

```bash
python flexible_module_report.py --date 25-05-05 --all-modules 1 2 3 4 5 6 7 8 9 10 --subset-modules 1 2 3 4 5 --output-prefix early_vs_late
```

This will generate a report comparing all modules (1-10) with early modules (1-5).

#### Count partial completions

```bash
python flexible_module_report.py --date 25-05-05 --count-partial
```

This will count labs with partial completion as fully completed labs, providing a more generous assessment of student progress. This is useful when you want to acknowledge students' efforts even if they haven't fully completed all lab requirements.

## Output

The script generates two output files in the `reports/YY-MM-DD/progress_reports/` directory:

1. **CSV Report**: `{output_prefix}.csv`
   - Contains the summary data for all students
   - Includes completion counts, percentages, and remaining labs

2. **Excel Report**: `{output_prefix}.xlsx`
   - Contains multiple sheets:
     - **Summary**: Overall student performance data
     - **Module X**: Individual sheets for each module showing student performance
     - **Configuration**: Details about which modules were included and how the report was generated

3. **Standardized Copy**: `progress_report_YY-MM-DD_Month-DD-YYYY_at_HH-MM-AM/PM.xlsx`
   - A copy of the Excel report with a standardized naming convention
   - Includes a human-readable timestamp for easy identification
   - Created automatically when a custom output prefix is used

## Data Source

The report generator uses data from the processed JSON files in the `assets/processed/YY-MM-DD/` directory. Specifically, it uses the `classgradebook-*.json` file to extract lab completion data for each student.

## Understanding the Report

### Main Summary Sheet

The main summary sheet in the Excel report includes the following columns:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Modules X-Y-Z Completed**: Number of labs completed across all specified modules
- **Total Modules X-Y-Z Labs**: Total number of labs across all specified modules
- **Modules X-Y-Z Remaining**: Number of labs still to be completed
- **Modules X-Y-Z Completion %**: Percentage of labs completed
- **Modules A-B-C Completed**: Number of labs completed across the subset modules
- **Total Modules A-B-C Labs**: Total number of labs across the subset modules
- **Modules A-B-C Remaining**: Number of labs still to be completed in the subset
- **Modules A-B-C Completion %**: Percentage of labs completed in the subset

### Module-specific Sheets

Each module has its own sheet in the Excel report, showing:

- **Student Name**: The name of the student
- **Email**: The student's email address
- **Module X Labs Completed**: Number of labs completed for this module
- **Total Module X Labs**: Total number of labs in this module
- **Completion Percentage**: Percentage of labs completed for this module
- **Labs Behind**: Number of labs still to be completed

All students are included in each module sheet, even if they have no data for that module.

## Integration with Other Tools

The Flexible Module Report Generator is designed to work with the other tools in the CompTIA reporting system:

1. First, process the raw CSV files:
   ```bash
   python csv_parser.py --date YY-MM-DD
   ```

2. Generate the basic module reports:
   ```bash
   python generate_reports.py --date YY-MM-DD --all
   ```

3. Generate the flexible module report:
   ```bash
   python flexible_module_report.py --date YY-MM-DD [options]
   ```

## Troubleshooting

If you encounter any issues with the report generator:

1. **Missing data**: Ensure that the CSV parser has been run for the specified date
2. **No labs found**: Check that the classgradebook JSON file exists in the processed directory
3. **Empty reports**: Verify that the modules specified actually contain lab activities

## Limitations

- The report generator only works with data that has been processed by the CSV parser
- Module numbers must be integers between 1 and 14
- The script assumes that lab names follow the pattern "Lab - X.Y.Z" where X is the module number

## Future Enhancements

Potential future enhancements to the report generator include:

- Support for custom date ranges
- Additional statistical analysis
- Student grouping and filtering options
- Graphical visualizations of student progress
