#!/usr/bin/env python3
"""
Report Generator

This script coordinates the entire reporting process:
1. Collects metrics using metrics_collector.py
2. Formats reports using report_formatter.py
3. Generates individual and/or class reports
"""

import os
import argparse
import subprocess
import json
from datetime import datetime

def run_metrics_collector(date_folder, output_prefix):
    """
    Run the metrics collector to gather data.
    
    Args:
        date_folder (str): The date folder to process (format: YY-MM-DD)
        output_prefix (str): Prefix for the output files
    
    Returns:
        str: Path to the generated metrics file
    """
    print(f"Collecting metrics for date folder: {date_folder}")
    
    # Use the metrics collector module directly instead of running a subprocess
    from compita.collectors.metrics_collector import collect_metrics
    
    # Call the metrics collector
    metrics = collect_metrics(date_folder)
    
    # Define the output path
    output_dir = f"reports/{date_folder}/metrics"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{output_prefix}.json"
    
    # Save the metrics to a file
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Metrics saved to: {output_file}")
    return output_file

def load_metrics_data(metrics_file):
    """
    Load metrics data from a file, handling both direct data and path references.
    
    Args:
        metrics_file (str): Path to the metrics file
        
    Returns:
        dict: Metrics data or None if loading failed
    """
    try:
        with open(metrics_file, 'r') as f:
            content = f.read().strip()
            
            # Check if the content is a JSON object or a path
            if content.startswith('{') and content.endswith('}'):
                # Direct JSON data
                return json.loads(content)
            elif content.startswith('"') and content.endswith('"'):
                # Path to another JSON file
                referenced_file = content.strip('"')
                if os.path.exists(referenced_file):
                    with open(referenced_file, 'r') as ref_f:
                        return json.load(ref_f)
                else:
                    print(f"Referenced metrics file not found: {referenced_file}")
                    return None
            else:
                # Try to parse as JSON anyway
                return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading metrics file: {e}")
        return None

def run_report_formatter(metrics_file, output_dir, student=None, class_summary=False):
    """
    Run the report formatter to generate reports.
    
    Args:
        metrics_file (str): Path to the metrics file
        output_dir (str): Directory to save the reports
        student (str, optional): Name of a specific student to generate a report for
        class_summary (bool): Whether to generate a class summary report
    
    Returns:
        list: Paths to the generated report files
    """
    print(f"Formatting reports from metrics file: {metrics_file}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load metrics data using the new helper function
    metrics_data = load_metrics_data(metrics_file)
    
    if not metrics_data:
        print("Failed to load metrics data. Aborting report generation.")
        return []
    
    # Import the markdown formatter module
    try:
        from compita.formatters.markdown_formatter import format_student_report, format_class_summary
        
        # Use the imported modules directly
        output_paths = []
        
        # Generate student report
        if student:
            # Get student data from metrics
            if isinstance(metrics_data, dict):
                student_data = None
                if 'student_metrics' in metrics_data and student in metrics_data['student_metrics']:
                    student_data = metrics_data['student_metrics'][student]
                elif student in metrics_data:
                    student_data = metrics_data[student]
                
                if student_data:
                    # Format student name for filename
                    student_filename = student.replace(', ', '_').replace(' ', '_')
                    output_file = os.path.join(output_dir, f"student_{student_filename}.md")
                    
                    # Format and save the report
                    report_content = format_student_report(student, student_data, metrics_data)
                    with open(output_file, 'w') as f:
                        f.write(report_content)
                    
                    print(f"Student report for {student} saved to: {output_file}")
                    output_paths.append(output_file)
                else:
                    print(f"No data found for student: {student}")
        
        # Generate class summary
        if class_summary:
            output_file = os.path.join(output_dir, "class_summary.md")
            
            # Format and save the report
            report_content = format_class_summary(metrics_data)
            with open(output_file, 'w') as f:
                f.write(report_content)
            
            print(f"Class summary report saved to: {output_file}")
            output_paths.append(output_file)
        
        return output_paths
        
    except ImportError:
        print("Could not import markdown formatter module. Using subprocess fallback.")
        # Build the command
        cmd = [
            "python", "report_formatter.py",
            "--metrics-file", metrics_file,
            "--output-dir", output_dir
        ]
        
        if student:
            cmd.extend(["--student", student])
        
        if class_summary:
            cmd.append("--class-summary")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running report formatter: {result.stderr}")
            return []
        
        # Extract the output paths from the output
        output_paths = []
        for line in result.stdout.split('\n'):
            if "report saved to:" in line:
                output_paths.append(line.split("report saved to:")[1].strip())
        
        return output_paths

def generate_reports(date_folder, output_dir, students=None, class_summary=False):
    """
    Generate reports for the specified date folder.
    
    Args:
        date_folder (str): The date folder to process (format: YY-MM-DD)
        output_dir (str): Directory to save the reports
        students (list, optional): List of student names to generate reports for
        class_summary (bool): Whether to generate a class summary report
    
    Returns:
        list: Paths to the generated report files
    """
    # Collect metrics
    metrics_file = run_metrics_collector(date_folder, "metrics")
    
    if not metrics_file:
        print("Failed to collect metrics. Aborting report generation.")
        return []
    
    # Load metrics data using the new helper function
    metrics_data = load_metrics_data(metrics_file)
    
    if not metrics_data:
        print("Failed to load metrics data. Aborting report generation.")
        return []
    
    # If no specific students are provided, generate reports for all students
    if students is None:
        if isinstance(metrics_data, dict):
            if 'student_metrics' in metrics_data:
                # Original format
                students = list(metrics_data['student_metrics'].keys())
            else:
                # New format - student names are top-level keys
                # Filter out any non-student keys (like metadata)
                students = [key for key in metrics_data.keys() if isinstance(metrics_data[key], dict) and 'modules' in metrics_data[key]]
                
                if not students:
                    print("Invalid metrics data format. Cannot determine student list.")
                    return []
        else:
            print("Invalid metrics data format. Cannot determine student list.")
            return []
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate reports
    report_files = []
    
    # Generate student reports
    if not class_summary and students:
        for student in students:
            # Use the exact output directory provided
            report_file = run_report_formatter(metrics_file, output_dir, student=student)
            if report_file:
                report_files.extend(report_file)
    
    # Generate class summary report
    if class_summary:
        # Use the exact output directory provided
        report_file = run_report_formatter(metrics_file, output_dir, class_summary=True)
        if report_file:
            report_files.extend(report_file)
    
    return report_files

def main():
    """
    Main function to parse command line arguments and execute the report generator.
    """
    parser = argparse.ArgumentParser(description='Generate comprehensive student progress reports.')
    parser.add_argument('--date', required=True, help='Date folder to process (format: YY-MM-DD)')
    parser.add_argument('--output-dir', default="reports", help='Directory to save the reports')
    parser.add_argument('--students', nargs='+', help='List of student names to generate reports for')
    parser.add_argument('--class-summary', action='store_true', help='Generate class summary report')
    parser.add_argument('--all', action='store_true', help='Generate reports for all students')
    
    args = parser.parse_args()
    
    # Create the output directory path
    date_output_dir = os.path.join(args.output_dir, args.date, "progress_reports")
    
    # Generate reports
    if args.all:
        output_paths = generate_reports(args.date, date_output_dir, class_summary=args.class_summary)
    else:
        output_paths = generate_reports(args.date, date_output_dir, students=args.students, class_summary=args.class_summary)
    
    if output_paths:
        print(f"Report generation complete! Generated {len(output_paths)} reports:")
        for path in output_paths:
            print(f"  - {path}")
    else:
        print("No reports were generated.")

if __name__ == "__main__":
    main()

# Add adapter functions for the new CLI interface
def generate_student_reports(date, output_dir=None, students=None):
    """
    Generate student reports for the specified date.
    
    Args:
        date (str): Date in YY-MM-DD format
        output_dir (str, optional): Directory to save the reports
        students (list, optional): List of student names to generate reports for
        
    Returns:
        list: Paths to the generated report files
    """
    # Set default output directory
    if output_dir is None:
        output_dir = f"reports/{date}/progress_reports/student_reports"
    
    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate reports
    return generate_reports(date, output_dir, students=students)

def generate_class_summary(date, output_dir=None):
    """
    Generate a class summary report for the specified date.
    
    Args:
        date (str): Date in YY-MM-DD format
        output_dir (str, optional): Directory to save the report
        
    Returns:
        str: Path to the generated report file
    """
    # Set default output directory
    if output_dir is None:
        output_dir = f"reports/{date}/progress_reports/class_summaries"
    
    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate report
    return generate_reports(date, output_dir, class_summary=True)