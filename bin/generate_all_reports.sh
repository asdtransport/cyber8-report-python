#!/bin/bash
# File: generate_all_reports.sh
# Description: Complete end-to-end script for generating all reports

# Set the date parameter (change this as needed)
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
