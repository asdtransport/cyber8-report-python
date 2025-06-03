"""
Utility functions for format conversion.
"""
import os
import re
from pathlib import Path

def extract_title_from_markdown(markdown_content):
    """
    Extract the title from a markdown document.
    
    Args:
        markdown_content (str): Markdown content
        
    Returns:
        str: Extracted title or default title if not found
    """
    # Look for a level 1 heading (# Title)
    title_match = re.search(r'^# (.+)$', markdown_content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    # If no level 1 heading, try to extract from filename
    return "Report"

def get_css_for_report_type(report_type):
    """
    Get the appropriate CSS for a specific report type.
    
    Args:
        report_type (str): Type of report ('student', 'class')
        
    Returns:
        str: CSS content
    """
    # Base CSS that applies to all reports
    base_css = """
    body {
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    h1, h2, h3, h4 {
        color: #2c3e50;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    h1 {
        text-align: center;
        font-size: 24pt;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    h2 {
        font-size: 18pt;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
    h3 {
        font-size: 14pt;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    """
    
    # Additional CSS for student reports
    student_css = """
    .executive-summary {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin: 20px 0;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 24pt;
        font-weight: bold;
        color: #3498db;
    }
    .student-rankings-table th, .student-rankings-table td {
        text-align: center;
    }
    .weekly-activity-table th:first-child, .weekly-activity-table td:first-child {
        width: 15%;
    }
    .weekly-activity-table th:nth-child(2), .weekly-activity-table td:nth-child(2) {
        width: 25%;
    }
    .module-progress-table th, .module-progress-table td {
        text-align: center;
    }
    """
    
    # Additional CSS for class reports
    class_css = """
    .class-summary {
        background-color: #f8f9fa;
        border-left: 4px solid #2ecc71;
        padding: 15px;
        margin: 20px 0;
    }
    .class-metrics {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    .class-metric-card {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .class-metric-value {
        font-size: 24pt;
        font-weight: bold;
        color: #2ecc71;
    }
    """
    
    if report_type == 'student':
        return base_css + student_css
    elif report_type == 'class':
        return base_css + class_css
    else:
        return base_css

def ensure_output_directory(output_dir):
    """
    Ensure the output directory exists.
    
    Args:
        output_dir (str): Output directory path
        
    Returns:
        Path: Path object for the output directory
    """
    path = Path(output_dir)
    os.makedirs(path, exist_ok=True)
    return path
