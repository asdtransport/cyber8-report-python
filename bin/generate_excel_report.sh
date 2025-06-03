#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Set current module to 6
CURRENT_MODULE=6

# Generate Excel report with multiple sheets
echo "Generating Excel report with all modules..."
python generate_reports.py --output "reports/student_progress_report.xlsx" --current-module $CURRENT_MODULE --excel

echo "Excel report generated successfully!"
