"""
Utility functions for report generation.
"""
import os
import datetime
from pathlib import Path

def format_date(date_str, output_format='%B %d, %Y'):
    """
    Format a date string from YY-MM-DD to a more readable format.
    
    Args:
        date_str (str): Date string in YY-MM-DD format
        output_format (str): Output date format
        
    Returns:
        str: Formatted date string
    """
    try:
        # Parse the date string
        date_obj = datetime.datetime.strptime(date_str, '%y-%m-%d')
        
        # Format the date
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str

def get_report_filename(student_name, date_str, report_type='student'):
    """
    Generate a standardized filename for a report.
    
    Args:
        student_name (str): Student name (for student reports)
        date_str (str): Date string in YY-MM-DD format
        report_type (str): Type of report ('student', 'class', 'module')
        
    Returns:
        str: Standardized filename
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    if report_type == 'student':
        # Replace spaces and commas with underscores
        safe_name = student_name.replace(' ', '_').replace(',', '').strip()
        return f"student_{safe_name}_report_{date_str}_{timestamp}.md"
    elif report_type == 'class':
        return f"class_summary_report_{date_str}_{timestamp}.md"
    elif report_type == 'module':
        return f"module_report_{date_str}_{timestamp}.md"
    else:
        return f"{report_type}_report_{date_str}_{timestamp}.md"

def ensure_report_directories(date_str):
    """
    Ensure all report directories exist for the specified date.
    
    Args:
        date_str (str): Date string in YY-MM-DD format
        
    Returns:
        dict: Dictionary of directory paths
    """
    # Base reports directory
    reports_dir = Path('reports') / date_str
    
    # Create subdirectories
    directories = {
        'base': reports_dir,
        'progress': reports_dir / 'progress_reports',
        'student': reports_dir / 'progress_reports' / 'student_reports',
        'class': reports_dir / 'progress_reports' / 'class_summaries',
        'assessment': reports_dir / 'assessment_reports',
        'grades': reports_dir / 'grades_reports',
        'executive': reports_dir / 'executive_reports',
        'metrics': reports_dir / 'metrics',
    }
    
    # Create all directories
    for dir_path in directories.values():
        os.makedirs(dir_path, exist_ok=True)
    
    return directories
