#!/usr/bin/env python3
"""
Markdown Formatter

This module formats student and class data into markdown reports.
"""

import os
import json
import datetime
import logging
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_time_seconds(seconds: int) -> str:
    """
    Format seconds into a human-readable string (e.g., "1h 30m 45s").
    
    Args:
        seconds (int): Number of seconds
        
    Returns:
        str: Formatted time string
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def format_student_report(student_name: str, student_data: Dict[str, Any], metrics_data: Dict[str, Any]) -> str:
    """
    Format student data into a markdown report.
    
    Args:
        student_name (str): Name of the student
        student_data (Dict[str, Any]): Student metrics data
        metrics_data (Dict[str, Any]): All metrics data
        
    Returns:
        str: Markdown report content
    """
    # Get current date for the report
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Start building the report
    report = []
    
    # Add header
    report.append(f"# Student Progress Report: {student_name}")
    report.append(f"**Generated on:** {current_date}")
    report.append("")
    
    # Add student information
    if 'email' in student_data:
        report.append(f"**Email:** {student_data['email']}")
        report.append("")
    
    # Add summary section
    report.append("## Summary")
    report.append("")
    
    if 'summary' in student_data:
        summary = student_data['summary']
        
        # Add overall progress
        if 'progress_score' in summary:
            completion_rate = summary['progress_score']
            report.append(f"**Overall Completion Rate:** {completion_rate:.1f}%")
        
        # Add average assessment score
        if 'assessments_avg_score' in summary:
            assessment_avg = summary['assessments_avg_score']
            report.append(f"**Average Assessment Score:** {assessment_avg:.1f}%")
        
        # Add total study time
        if 'study_time' in student_data and 'total_seconds' in student_data['study_time']:
            study_time = format_time_seconds(student_data['study_time']['total_seconds'])
            report.append(f"**Total Study Time:** {study_time}")
        
        # Add total study days
        if 'total_study_days' in summary:
            study_days = summary['total_study_days']
            report.append(f"**Total Study Days:** {study_days}")
    
    report.append("")
    
    # Add module progress section
    report.append("## Module Progress")
    report.append("")
    
    if 'modules' in student_data:
        modules = student_data['modules']
        
        # Create module progress table
        report.append("| Module | Labs Completed | Labs Completion | Assessments Avg | Assessments Completion |")
        report.append("|--------|---------------|-----------------|-----------------|------------------------|")
        
        for module_num, module_data in sorted(modules.items(), key=lambda x: int(x[0])):
            labs_completed = module_data.get('labs_completed', 0)
            labs_total = module_data.get('labs_total', 0)
            labs_rate = module_data.get('labs_completion_rate', 0)
            
            assessments_avg = module_data.get('assessments_avg_score', 0)
            assessments_rate = module_data.get('assessments_completion_rate', 0)
            
            report.append(f"| {module_num} | {labs_completed}/{labs_total} | {labs_rate:.1f}% | {assessments_avg:.1f}% | {assessments_rate:.1f}% |")
    
    report.append("")
    
    # Add weekly activity section
    report.append("## Weekly Activity")
    report.append("")
    
    if 'weekly_metrics' in student_data:
        weekly_metrics = student_data['weekly_metrics']
        
        # Create weekly activity table
        report.append("| Week | Study Time | Study Days |")
        report.append("|------|------------|------------|")
        
        for week_num, week_data in sorted(weekly_metrics.items(), key=lambda x: int(x[0])):
            study_time = format_time_seconds(week_data.get('study_time_seconds', 0))
            study_days = week_data.get('study_days', 0)
            
            report.append(f"| {week_num} | {study_time} | {study_days} |")
    
    report.append("")
    
    # Add recommendations section
    report.append("## Recommendations")
    report.append("")
    report.append("Based on your progress, we recommend focusing on the following areas:")
    report.append("")
    
    # Generate recommendations based on module completion rates
    if 'modules' in student_data:
        modules = student_data['modules']
        
        # Find modules with low completion rates
        low_completion_modules = []
        for module_num, module_data in modules.items():
            if module_data.get('labs_completion_rate', 100) < 80:
                low_completion_modules.append((module_num, module_data.get('labs_completion_rate', 0)))
        
        # Sort by completion rate (lowest first)
        low_completion_modules.sort(key=lambda x: x[1])
        
        # Add recommendations for up to 3 modules
        for module_num, completion_rate in low_completion_modules[:3]:
            report.append(f"- **Module {module_num}**: Complete remaining labs to improve your completion rate ({completion_rate:.1f}%).")
    
    report.append("")
    report.append("---")
    report.append("*This report was generated automatically by the Cyber8 Report Generator.*")
    
    return "\n".join(report)

def format_class_summary(metrics_data: Dict[str, Any]) -> str:
    """
    Format class metrics data into a markdown report.
    
    Args:
        metrics_data (Dict[str, Any]): All metrics data
        
    Returns:
        str: Markdown report content
    """
    # Get current date for the report
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Start building the report
    report = []
    
    # Add header
    report.append("# Class Summary Report")
    report.append(f"**Generated on:** {current_date}")
    report.append("")
    
    # Add class overview section
    report.append("## Class Overview")
    report.append("")
    
    # Count number of students
    student_count = 0
    if 'student_metrics' in metrics_data:
        student_count = len(metrics_data['student_metrics'])
    else:
        # New format - student names are top-level keys
        # Filter out any non-student keys (like metadata)
        student_count = len([key for key in metrics_data.keys() if isinstance(metrics_data[key], dict) and 'modules' in metrics_data[key]])
    
    report.append(f"**Total Students:** {student_count}")
    report.append("")
    
    # Add student rankings section
    report.append("## Student Rankings")
    report.append("")
    
    # Create student rankings table
    report.append("| Rank | Student | Overall Completion | Avg Assessment Score | Total Study Time |")
    report.append("|------|---------|-------------------|----------------------|------------------|")
    
    # Collect student summary data
    student_summaries = []
    
    if 'student_metrics' in metrics_data:
        # Original format
        for student_name, student_data in metrics_data['student_metrics'].items():
            if 'summary' in student_data:
                summary = student_data['summary']
                student_summaries.append({
                    'name': student_name,
                    'completion_rate': summary.get('progress_score', 0),
                    'assessment_avg': summary.get('assessments_avg_score', 0),
                    'study_time': student_data.get('study_time', {}).get('total_seconds', 0)
                })
    else:
        # New format - student names are top-level keys
        for student_name, student_data in metrics_data.items():
            if isinstance(student_data, dict) and 'summary' in student_data:
                summary = student_data['summary']
                student_summaries.append({
                    'name': student_name,
                    'completion_rate': summary.get('progress_score', 0),
                    'assessment_avg': summary.get('assessments_avg_score', 0),
                    'study_time': student_data.get('study_time', {}).get('total_seconds', 0)
                })
    
    # Sort by completion rate (highest first)
    student_summaries.sort(key=lambda x: x['completion_rate'], reverse=True)
    
    # Add student rankings to the table
    for i, student in enumerate(student_summaries):
        rank = i + 1
        name = student['name']
        completion_rate = student['completion_rate']
        assessment_avg = student['assessment_avg']
        study_time = format_time_seconds(student['study_time'])
        
        report.append(f"| {rank} | {name} | {completion_rate:.1f}% | {assessment_avg:.1f}% | {study_time} |")
    
    report.append("")
    
    # Add module completion section
    report.append("## Module Completion")
    report.append("")
    
    # Create module completion table
    report.append("| Module | Avg Labs Completion | Avg Assessment Score |")
    report.append("|--------|---------------------|----------------------|")
    
    # Collect module completion data
    module_data = {}
    
    if 'student_metrics' in metrics_data:
        # Original format
        for student_name, student_data in metrics_data['student_metrics'].items():
            if 'modules' in student_data:
                for module_num, mod_data in student_data['modules'].items():
                    if module_num not in module_data:
                        module_data[module_num] = {
                            'labs_completion': [],
                            'assessment_avg': []
                        }
                    
                    if 'labs_completion_rate' in mod_data:
                        module_data[module_num]['labs_completion'].append(mod_data['labs_completion_rate'])
                    
                    if 'assessments_avg_score' in mod_data:
                        module_data[module_num]['assessment_avg'].append(mod_data['assessments_avg_score'])
    else:
        # New format - student names are top-level keys
        for student_name, student_data in metrics_data.items():
            if isinstance(student_data, dict) and 'modules' in student_data:
                for module_num, mod_data in student_data['modules'].items():
                    if module_num not in module_data:
                        module_data[module_num] = {
                            'labs_completion': [],
                            'assessment_avg': []
                        }
                    
                    if 'labs_completion_rate' in mod_data:
                        module_data[module_num]['labs_completion'].append(mod_data['labs_completion_rate'])
                    
                    if 'assessments_avg_score' in mod_data:
                        module_data[module_num]['assessment_avg'].append(mod_data['assessments_avg_score'])
    
    # Calculate averages and add to the table
    for module_num, data in sorted(module_data.items(), key=lambda x: int(x[0])):
        labs_completion = data['labs_completion']
        assessment_avg = data['assessment_avg']
        
        avg_labs_completion = sum(labs_completion) / len(labs_completion) if labs_completion else 0
        avg_assessment_score = sum(assessment_avg) / len(assessment_avg) if assessment_avg else 0
        
        report.append(f"| {module_num} | {avg_labs_completion:.1f}% | {avg_assessment_score:.1f}% |")
    
    report.append("")
    
    # Add weekly activity section
    report.append("## Weekly Activity")
    report.append("")
    
    # Create weekly activity table
    report.append("| Week | Avg Study Time | Avg Study Days | Active Students |")
    report.append("|------|---------------|----------------|-----------------|")
    
    # Collect weekly activity data
    weekly_data = {}
    
    if 'student_metrics' in metrics_data:
        # Original format
        for student_name, student_data in metrics_data['student_metrics'].items():
            if 'weekly_metrics' in student_data:
                for week_num, week_data in student_data['weekly_metrics'].items():
                    if week_num not in weekly_data:
                        weekly_data[week_num] = {
                            'study_time': [],
                            'study_days': [],
                            'active_students': 0
                        }
                    
                    if 'study_time_seconds' in week_data and week_data['study_time_seconds'] > 0:
                        weekly_data[week_num]['study_time'].append(week_data['study_time_seconds'])
                        weekly_data[week_num]['active_students'] += 1
                    
                    if 'study_days' in week_data:
                        weekly_data[week_num]['study_days'].append(week_data['study_days'])
    else:
        # New format - student names are top-level keys
        for student_name, student_data in metrics_data.items():
            if isinstance(student_data, dict) and 'weekly_metrics' in student_data:
                for week_num, week_data in student_data['weekly_metrics'].items():
                    if week_num not in weekly_data:
                        weekly_data[week_num] = {
                            'study_time': [],
                            'study_days': [],
                            'active_students': 0
                        }
                    
                    if 'study_time_seconds' in week_data and week_data['study_time_seconds'] > 0:
                        weekly_data[week_num]['study_time'].append(week_data['study_time_seconds'])
                        weekly_data[week_num]['active_students'] += 1
                    
                    if 'study_days' in week_data:
                        weekly_data[week_num]['study_days'].append(week_data['study_days'])
    
    # Calculate averages and add to the table
    for week_num, data in sorted(weekly_data.items(), key=lambda x: int(x[0])):
        study_time = data['study_time']
        study_days = data['study_days']
        active_students = data['active_students']
        
        avg_study_time_seconds = sum(study_time) / len(study_time) if study_time else 0
        avg_study_days = sum(study_days) / len(study_days) if study_days else 0
        
        avg_study_time = format_time_seconds(int(avg_study_time_seconds))
        
        report.append(f"| {week_num} | {avg_study_time} | {avg_study_days:.1f} | {active_students} |")
    
    report.append("")
    report.append("---")
    report.append("*This report was generated automatically by the Cyber8 Report Generator.*")
    
    return "\n".join(report)

def main():
    """
    Main function to parse command line arguments and generate reports.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate markdown reports from metrics data.')
    parser.add_argument('--metrics-file', required=True, help='Path to the metrics JSON file')
    parser.add_argument('--output-dir', required=True, help='Directory to save the reports')
    parser.add_argument('--student', help='Name of a specific student to generate a report for')
    parser.add_argument('--class-summary', action='store_true', help='Generate class summary report')
    parser.add_argument('--all', action='store_true', help='Generate reports for all students')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load metrics data
    try:
        with open(args.metrics_file, 'r') as f:
            metrics_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading metrics file: {e}")
        return
    
    # Generate student report
    if args.student:
        # Get student data from metrics
        if isinstance(metrics_data, dict):
            student_data = None
            if 'student_metrics' in metrics_data and args.student in metrics_data['student_metrics']:
                student_data = metrics_data['student_metrics'][args.student]
            elif args.student in metrics_data:
                student_data = metrics_data[args.student]
            
            if student_data:
                # Format student name for filename
                student_filename = args.student.replace(', ', '_').replace(' ', '_')
                output_file = os.path.join(args.output_dir, f"student_{student_filename}.md")
                
                # Format and save the report
                report_content = format_student_report(args.student, student_data, metrics_data)
                with open(output_file, 'w') as f:
                    f.write(report_content)
                
                print(f"Student report for {args.student} saved to: {output_file}")
            else:
                print(f"No data found for student: {args.student}")
    
    # Generate reports for all students
    if args.all:
        students = []
        if isinstance(metrics_data, dict):
            if 'student_metrics' in metrics_data:
                students = list(metrics_data['student_metrics'].keys())
            else:
                # New format - student names are top-level keys
                # Filter out any non-student keys (like metadata)
                students = [key for key in metrics_data.keys() if isinstance(metrics_data[key], dict) and 'modules' in metrics_data[key]]
        
        for student in students:
            # Get student data from metrics
            student_data = None
            if 'student_metrics' in metrics_data:
                student_data = metrics_data['student_metrics'].get(student)
            else:
                student_data = metrics_data.get(student)
            
            if student_data:
                # Format student name for filename
                student_filename = student.replace(', ', '_').replace(' ', '_')
                output_file = os.path.join(args.output_dir, f"student_{student_filename}.md")
                
                # Format and save the report
                report_content = format_student_report(student, student_data, metrics_data)
                with open(output_file, 'w') as f:
                    f.write(report_content)
                
                print(f"Student report for {student} saved to: {output_file}")
    
    # Generate class summary
    if args.class_summary:
        output_file = os.path.join(args.output_dir, "class_summary.md")
        
        # Format and save the report
        report_content = format_class_summary(metrics_data)
        with open(output_file, 'w') as f:
            f.write(report_content)
        
        print(f"Class summary report saved to: {output_file}")

if __name__ == "__main__":
    main()
