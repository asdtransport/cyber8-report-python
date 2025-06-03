#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Set current module to 6
CURRENT_MODULE=6

# Generate reports for modules 1-6
for module in {1..6}; do
  echo "Generating report for Module $module..."
  python generate_reports.py --module $module --output "reports/module${module}_report.csv" --current-module $CURRENT_MODULE
done

# Generate class report
echo "Generating class report..."
python generate_reports.py --output "reports/class_report.csv" --current-module $CURRENT_MODULE

echo "All reports generated successfully!"
