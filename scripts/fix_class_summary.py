#!/usr/bin/env python3
"""
Fix the class summary report table formatting.
This script directly modifies the class summary markdown file to create a cleaner table.
"""

import os
import re
import sys
import argparse
from markdown_to_pdf import MarkdownToPDF

def fix_overall_score_table(markdown_content):
    """
    Fix the Overall Score table in class summary reports.
    
    Args:
        markdown_content (str): Markdown content
        
    Returns:
        str: Fixed markdown content
    """
    # Find the Overall Score section
    overall_score_match = re.search(r'## Overall Score\s+(.*?)(?=##|\Z)', markdown_content, re.DOTALL)
    
    if overall_score_match:
        overall_score_section = overall_score_match.group(0)
        
        # Create a new, cleaner table with HTML
        new_table = """## Overall Score

| Student | Score |
|---------|-------|
"""
        
        # Extract rows from the original table
        rows = re.findall(r'\|(.*?)\|(.*?)\|', overall_score_section)
        
        # Skip the header row if it exists
        start_idx = 1 if len(rows) > 0 and ('Student' in rows[0][0] or 'student' in rows[0][0].lower()) else 0
        
        for row in rows[start_idx:]:
            if len(row) >= 2:
                student = row[0].strip()
                score = row[1].strip()
                new_table += f"| {student} | {score} |\n"
        
        # Replace the original table with the new one
        markdown_content = markdown_content.replace(overall_score_section, new_table)
    
    return markdown_content

def main():
    """Main function to fix class summary report and generate PDF."""
    parser = argparse.ArgumentParser(description='Fix class summary report and generate PDF')
    parser.add_argument('--input-dir', required=True, help='Directory containing markdown files')
    parser.add_argument('--output-dir', required=True, help='Directory to save PDF files')
    args = parser.parse_args()
    
    # Find class summary report
    class_summary_path = None
    for root, _, files in os.walk(args.input_dir):
        for file in files:
            if 'class_summary' in file.lower() and file.endswith('.md'):
                class_summary_path = os.path.join(root, file)
                break
        if class_summary_path:
            break
    
    if not class_summary_path:
        print("Error: Class summary report not found")
        sys.exit(1)
    
    # Read the class summary report
    with open(class_summary_path, 'r') as f:
        content = f.read()
    
    # Fix the Overall Score table
    fixed_content = fix_overall_score_table(content)
    
    # Create a temporary file with the fixed content
    temp_file = os.path.join(os.path.dirname(class_summary_path), 'fixed_class_summary.md')
    with open(temp_file, 'w') as f:
        f.write(fixed_content)
    
    # Convert the fixed markdown to PDF
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'class_summary_report.pdf')
    
    converter = MarkdownToPDF(os.path.dirname(temp_file), args.output_dir)
    
    # First convert the file using the convert_file method
    converter.convert_file(temp_file, is_class_summary=True)
    
    print(f"Fixed class summary report generated: {output_file}")
    
    # Remove the temporary file
    os.remove(temp_file)

if __name__ == "__main__":
    main()
