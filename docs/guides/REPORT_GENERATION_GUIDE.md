# Complete End-to-End Report Generation Guide

This guide walks you through the entire process of generating student and class reports from raw CSV data to final PDF documents, including generating CSV module reports using the `generate_reports.py` script.

## Step 1: Parse CSV Files to JSON

First, convert the raw CSV files into structured JSON format:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Process gradebook data
python csv_parser.py --date 25-05-05 --file_type classgradebook --parser_type gradebook

# Process study history data
python csv_parser.py --date 25-05-05 --file_type studyhistory --parser_type study

# Process time per resource data
python csv_parser.py --date 25-05-05 --file_type timeperresource --parser_type resource
```

This creates JSON files in the `assets/processed/25-05-05` directory:
- `classgradebook-5-05-5pm.json`
- `classstudyhistory-05-05-4pm.json`
- `timeperresource-05-05-5pm.json`

## Step 2: Generate Flexible Reports

Before proceeding to the general CSV module reports, you can generate specialized flexible reports that provide detailed analysis of student performance:

```bash
# Generate flexible module completion report
python flexible_module_report.py --date 25-05-05

# Generate flexible assessment (study time) report
python flexible_assessment_report.py --date 25-05-05

# Generate flexible grades report
python flexible_grades_report.py --date 25-05-05
```

These commands will generate specialized reports in their respective directories:
- Module completion reports in `reports/25-05-05/progress_reports/`
- Assessment (study time) reports in `reports/25-05-05/assessment_reports/`
- Grades reports in `reports/25-05-05/grades_reports/`

Each flexible report provides detailed analysis with both CSV and Excel formats, allowing for customized filtering and analysis of student data.

### Flexible Report Options

Each flexible report offers various customization options:

**Flexible Module Report**:
```bash
# Custom module selection
python flexible_module_report.py --date 25-05-05 --all-modules 1 2 4 5 --subset-modules 4 5

# Exclude specific modules
python flexible_module_report.py --date 25-05-05 --exclude-modules 3

# Count partial completions as fully completed
python flexible_module_report.py --date 25-05-05 --count-partial
```

**Flexible Assessment Report**:
```bash
# Custom date ranges
python flexible_assessment_report.py --date 25-05-05 --date-range "Apr 15 May 5" --subset-range "Apr 15 Apr 30"

# Set minimum study threshold
python flexible_assessment_report.py --date 25-05-05 --min-study-threshold 300
```

**Flexible Grades Report**:
```bash
# Custom module selection and assessment types
python flexible_grades_report.py --date 25-05-05 --all-modules 1 2 3 --assessment-types "Module Quiz" "Lesson Review"

# Set minimum grade threshold
python flexible_grades_report.py --date 25-05-05 --min-grade-threshold 0.8
```

## Step 3: Generate CSV Module Reports

Before proceeding to metrics collection, you can generate detailed CSV module reports using the `generate_reports.py` script:

```bash
# Generate all reports (module reports, student reports, class report, and Excel report)
python generate_reports.py --date 25-05-05 --all
```

This single command will generate:
- Individual module reports for each module (1-14) in `reports/25-05-05/module_X_report.csv`
- Individual student reports in `reports/25-05-05/student_[Name]_report.csv`
- A class summary report in `reports/25-05-05/class_report.csv`
- An Excel report with multiple sheets in `reports/25-05-05/class_report.xlsx`

These CSV and Excel reports provide detailed breakdowns of:
- Module completion rates by student
- Time spent on each module
- Individual student progress across all modules
- Time spent on specific resources

These reports are useful for detailed analysis and can be imported into spreadsheet software for further processing or visualization.

## Step 4: Collect and Combine Metrics

Next, collect and combine metrics from all data sources:

```bash
python metrics_collector.py --date 25-05-05
```

This step:
- Combines data from all three JSON sources
- Calculates summary metrics for each student
- Calculates module range metrics
- Saves the combined metrics to `reports/25-05-05/metrics/combined_metrics.json`

## Step 5: Generate Markdown Reports

Generate formatted markdown reports for students and class summary:

```bash
# Generate student reports
python report_generator.py --date 25-05-05

# Generate class summary report
python report_generator.py --date 25-05-05 --class-summary
```

This creates:
- Individual student reports in `reports/25-05-05/progress_reports/student_reports`
- Class summary report in `reports/25-05-05/progress_reports/class_summaries`

## Step 6: Convert Markdown to PDF

Finally, convert the markdown reports to professionally formatted PDF files:

```bash
# Convert student reports to PDF
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports/student_reports --output-dir reports/25-05-05/executive_reports

# Convert class summary report to PDF
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports/class_summaries --output-dir reports/25-05-05/executive_reports
```

This generates:
- 23 individual student PDF reports
- 1 class summary PDF report

All PDFs are saved to `reports/25-05-05/executive_reports` and are ready for presentation.

## Complete One-Line Command

To run the entire process with a single command, you can use:

```bash
source .venv/bin/activate && \
python csv_parser.py --date 25-05-05 --file_type classgradebook --parser_type gradebook && \
python csv_parser.py --date 25-05-05 --file_type studyhistory --parser_type study && \
python csv_parser.py --date 25-05-05 --file_type timeperresource --parser_type resource && \
python flexible_module_report.py --date 25-05-05 && \
python flexible_assessment_report.py --date 25-05-05 && \
python flexible_grades_report.py --date 25-05-05 && \
python generate_reports.py --date 25-05-05 --all && \
python metrics_collector.py --date 25-05-05 && \
python report_generator.py --date 25-05-05 && \
python report_generator.py --date 25-05-05 --class-summary && \
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports/student_reports --output-dir reports/25-05-05/executive_reports && \
python markdown_to_pdf.py --input-dir reports/25-05-05/progress_reports/class_summaries --output-dir reports/25-05-05/executive_reports
```

You can also create a shell script with these commands for easy execution:

```bash
#!/bin/bash
# File: generate_all_reports.sh

# Set the date parameter
DATE="25-05-05"

# Activate virtual environment
source .venv/bin/activate

# Step 1: Parse CSV files to JSON
echo "Step 1: Parsing CSV files to JSON..."
python csv_parser.py --date $DATE --file_type classgradebook --parser_type gradebook
python csv_parser.py --date $DATE --file_type studyhistory --parser_type study
python csv_parser.py --date $DATE --file_type timeperresource --parser_type resource

# Step 2: Generate flexible reports
echo "Step 2: Generating flexible reports..."
python flexible_module_report.py --date $DATE
python flexible_assessment_report.py --date $DATE
python flexible_grades_report.py --date $DATE

# Step 3: Generate CSV module reports
echo "Step 3: Generating CSV module reports..."
python generate_reports.py --date $DATE --all

# Step 4: Collect and combine metrics
echo "Step 4: Collecting and combining metrics..."
python metrics_collector.py --date $DATE

# Step 5: Generate markdown reports
echo "Step 5: Generating markdown reports..."
python report_generator.py --date $DATE
python report_generator.py --date $DATE --class-summary

# Step 6: Convert markdown to PDF
echo "Step 6: Converting markdown to PDF..."
python markdown_to_pdf.py --input-dir reports/$DATE/progress_reports/student_reports --output-dir reports/$DATE/executive_reports
python markdown_to_pdf.py --input-dir reports/$DATE/progress_reports/class_summaries --output-dir reports/$DATE/executive_reports

echo "Report generation complete!"
```

Make the script executable with `chmod +x generate_all_reports.sh` and run it with `./generate_all_reports.sh`.

## Output Files and Directories

After running the complete process, you'll have:

1. **JSON Data**:
   - `assets/processed/25-05-05/*.json`

2. **Flexible Reports**:
   - `reports/25-05-05/progress_reports/progress_report_*.csv` and `*.xlsx`
   - `reports/25-05-05/assessment_reports/assessment_report_*.csv` and `*.xlsx`
   - `reports/25-05-05/grades_reports/grades_report_*.csv` and `*.xlsx`

3. **CSV Module Reports**:
   - `reports/25-05-05/module_X_report.csv`
   - `reports/25-05-05/student_[Name]_report.csv`
   - `reports/25-05-05/class_report.csv`
   - `reports/25-05-05/class_report.xlsx`

4. **Combined Metrics**:
   - `reports/25-05-05/metrics/combined_metrics.json`
   - `reports/25-05-05/metrics/metrics_*.json`

5. **Markdown Reports**:
   - `reports/25-05-05/progress_reports/student_reports/*.md`
   - `reports/25-05-05/progress_reports/class_summaries/class_summary_report.md`

6. **PDF Reports**:
   - `reports/25-05-05/executive_reports/*.pdf`

This complete workflow ensures you have all the necessary data formats for analysis, presentation, and archiving.

## Troubleshooting

### Common Issues

1. **Missing Weekly Activity Data**
   - If a student's weekly activity data is missing, check for whitespace inconsistencies in student names across different data sources.
   - The system now strips whitespace from student names to ensure consistency.

2. **Duplicate Reports**
   - If you see duplicate reports for the same student (e.g., "Van,_Dafne_report.pdf" and "Van,_Dafne__report.pdf"), this indicates whitespace inconsistencies in the source data.
   - The latest version of the code handles this by normalizing student names.

3. **Empty Tables in Reports**
   - If a section in a report shows an empty table, it means there's no data for that section in the source files.
   - Verify that the corresponding data exists in the JSON files.

### Data Integrity Checks

Before generating reports, you can verify data integrity with:

```bash
# Check if a specific student exists in the combined metrics
python -c "import json; data = json.load(open('reports/25-05-05/metrics/combined_metrics.json')); print('Student in data:', 'Student Name' in data)"

# Check if a student has weekly activity data
python -c "import json; data = json.load(open('reports/25-05-05/metrics/combined_metrics.json')); print('Weekly metrics:', data['Student Name']['weekly_metrics'] if 'Student Name' in data else 'Not found')"
```

Replace 'Student Name' with the actual student name you want to check.
