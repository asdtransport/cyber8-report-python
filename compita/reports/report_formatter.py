#!/usr/bin/env python3
"""
Report Formatter

This script formats the combined metrics into markdown reports.
It provides various templates for different report types.
"""

import json
import os
import argparse
from datetime import datetime

class ReportFormatter:
    """
    A class to format metrics data into markdown reports.
    """
    
    def __init__(self, metrics_file):
        """
        Initialize the ReportFormatter with the specified metrics file.
        
        Args:
            metrics_file (str): Path to the combined metrics JSON file
        """
        self.metrics_file = metrics_file
        
        # Load the metrics data
        with open(metrics_file, 'r') as f:
            self.metrics_data = json.load(f)
    
    def format_student_report(self, student_name):
        """
        Format a report for a specific student.
        
        Args:
            student_name (str): Name of the student
        
        Returns:
            str: Markdown formatted report
        """
        # Check if student exists in metrics data
        if student_name not in self.metrics_data:
            return f"# Error: Student '{student_name}' not found in metrics data."
        
        student_data = self.metrics_data[student_name]
        
        # Debug print for student data
        with open("debug_output.txt", "a") as f:
            f.write(f"\n\nDEBUG - Student: {student_name}\n")
            f.write(f"Weekly metrics keys: {list(student_data['weekly_metrics'].keys())}\n")
            f.write(f"Weekly metrics data: {student_data['weekly_metrics']}\n")
        
        # Start building the report
        report = []
        report.append(f"# Progress Report: {student_name}")
        report.append(f"**Email:** {student_data['email']}")
        report.append(f"**Report Date:** {datetime.now().strftime('%B %d, %Y')}")
        report.append("")
        
        # Add summary section
        report.append("## Summary")
        report.append("")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Overall Score | {student_data['summary']['overall_score']:.1f}% |")
        report.append(f"| Progress Score | {student_data['summary']['progress_score']:.1f}% |")
        report.append(f"| Engagement Score | {student_data['summary']['engagement_score']:.1f}% |")
        report.append(f"| Labs Completed | {student_data['summary']['total_labs_completed']} / {student_data['summary']['total_labs']} ({student_data['summary']['labs_completion_rate']:.1f}%) |")
        report.append(f"| Assessments Completed | {student_data['summary']['total_assessments_completed']} / {student_data['summary']['total_assessments']} ({student_data['summary']['assessments_completion_rate']:.1f}%) |")
        report.append(f"| Assessment Average Score | {student_data['summary']['assessments_avg_score']:.1f}% |")
        report.append(f"| Total Study Time | {student_data['study_time'].get('total_formatted', 'N/A')} |")
        report.append(f"| Study Days | {student_data['study_time'].get('study_days', 0)} |")
        report.append(f"| Average Daily Study Time | {student_data['study_time'].get('avg_daily_formatted', 'N/A')} |")
        report.append("")
        
        # Add module progress section
        report.append("## Module Progress")
        report.append("")
        
        # Add module range summaries
        for range_name, range_data in student_data['module_ranges'].items():
            report.append(f"### {range_name.capitalize()} Modules ({'-'.join(str(m) for m in range_data['modules'])})")
            report.append("")
            report.append("| Metric | Value |")
            report.append("|--------|-------|")
            report.append(f"| Labs Completed | {range_data['labs_completed']} / {range_data['labs_total']} ({range_data['labs_completion_rate']:.1f}%) |")
            report.append(f"| Assessments Completed | {range_data['assessments_completed']} / {range_data['assessments_total']} ({range_data['assessments_completion_rate']:.1f}%) |")
            report.append(f"| Assessment Average Score | {range_data['assessments_avg_score']:.1f}% |")
            report.append("")
        
        # Add individual module details
        report.append("### Individual Module Details")
        report.append("")
        report.append("| Module | Labs Completed | Labs Completion % | Assessment Avg. Score | Assessment Completion % |")
        report.append("|--------|---------------|-------------------|------------------------|-------------------------|")
        
        # Sort module numbers numerically and handle both string and integer keys
        module_keys = student_data['modules'].keys()
        # Convert all keys to integers for sorting
        module_nums = [int(m) if isinstance(m, str) else m for m in module_keys]
        
        for module_num in sorted(module_nums):
            # Check if the key exists as integer or string
            if module_num in student_data['modules']:
                module_key = module_num
            else:
                module_key = str(module_num)
            
            module_data = student_data['modules'][module_key]
            report.append(f"| Module {module_num} | {module_data['labs_completed']} / {module_data['labs_total']} | {module_data['labs_completion_rate']:.1f}% | {module_data['assessments_avg_score']:.1f}% | {module_data['assessments_completion_rate']:.1f}% |")
        
        report.append("")
        
        # Add weekly activity section
        report.append("## Weekly Activity")
        report.append("")
        report.append("| Week | Study Time | Study Days | Labs Completed | Assessments Completed |")
        report.append("|------|------------|------------|----------------|------------------------|")
        
        # Sort week numbers numerically and handle both string and integer keys
        week_keys = student_data['weekly_metrics'].keys()
        # Convert all keys to integers for sorting
        week_nums = [int(w) if isinstance(w, str) else w for w in week_keys]
        
        # Add debug print to check week numbers
        print(f"DEBUG - Student: {student_name}, Week numbers: {sorted(week_nums)}")
        
        for week_num in sorted(week_nums):
            # Check if the key exists as integer or string
            if week_num in student_data['weekly_metrics']:
                week_key = week_num
            else:
                week_key = str(week_num)
            
            week_data = student_data['weekly_metrics'][week_key]
            labs_completed = week_data.get('labs_completed', 0)
            assessments_completed = week_data.get('assessments_completed', 0)
            report.append(f"| Week {week_num} | {week_data['study_time_formatted']} | {week_data['study_days']} | {labs_completed} | {assessments_completed} |")
        
        report.append("")
        
        # Add assessment types section
        report.append("## Assessment Performance")
        report.append("")
        report.append("| Assessment Type | Completed | Total | Avg. Score | Completion % |")
        report.append("|-----------------|-----------|-------|------------|--------------|")
        
        for assessment_type in sorted(student_data['assessments'].keys()):
            type_data = student_data['assessments'][assessment_type]
            report.append(f"| {assessment_type} | {type_data['completed']} | {type_data['total']} | {type_data['avg_score']:.1f}% | {type_data['completion_rate']:.1f}% |")
        
        report.append("")
        
        # Add recommendations section
        report.append("## Recommendations")
        report.append("")
        
        # Generate recommendations based on metrics
        if student_data['summary']['labs_completion_rate'] < 50:
            report.append("- **Focus on completing more labs**: Your lab completion rate is below 50%. Labs provide hands-on experience that is crucial for skill development.")
        
        if student_data['summary']['assessments_avg_score'] < 70:
            report.append("- **Review assessment material**: Your assessment average score is below 70%. Consider revisiting the material to strengthen your understanding.")
        
        if student_data['study_time'].get('study_days', 0) < 10:
            report.append("- **Increase study frequency**: You've studied on fewer than 10 days. Regular, consistent study is more effective than cramming.")
        
        if student_data['study_time'].get('total_seconds', 0) < 20 * 3600:  # Less than 20 hours
            report.append("- **Increase total study time**: Your total study time is less than 20 hours. Consider dedicating more time to master the material.")
        
        # Find modules with low completion rates
        low_completion_modules = []
        for module_num, module_data in student_data['modules'].items():
            if module_data['labs_completion_rate'] < 50 and module_data['labs_total'] > 0:
                low_completion_modules.append(module_num)
        
        if low_completion_modules:
            report.append(f"- **Focus on modules {', '.join(str(m) for m in sorted(low_completion_modules))}**: These modules have low completion rates and should be prioritized.")
        
        return "\n".join(report)
    
    def format_class_summary_report(self):
        """
        Format a summary report for the entire class.
        
        Returns:
            str: Markdown formatted report
        """
        # Start building the report
        report = []
        report.append("# Class Summary Report")
        report.append(f"**Report Date:** {datetime.now().strftime('%B %d, %Y')}")
        report.append("")
        
        # Add class summary section
        report.append("## Class Overview")
        report.append("")
        
        # Calculate class averages
        student_count = len(self.metrics_data)
        overall_score_avg = sum(data['summary']['overall_score'] for name, data in self.metrics_data.items()) / student_count if student_count > 0 else 0
        progress_score_avg = sum(data['summary']['progress_score'] for name, data in self.metrics_data.items()) / student_count if student_count > 0 else 0
        engagement_score_avg = sum(data['summary']['engagement_score'] for name, data in self.metrics_data.items()) / student_count if student_count > 0 else 0
        labs_completion_avg = sum(data['summary']['labs_completion_rate'] for name, data in self.metrics_data.items()) / student_count if student_count > 0 else 0
        assessments_completion_avg = sum(data['summary']['assessments_completion_rate'] for name, data in self.metrics_data.items()) / student_count if student_count > 0 else 0
        assessments_score_avg = sum(data['summary']['assessments_avg_score'] for name, data in self.metrics_data.items()) / student_count if student_count > 0 else 0
        
        report.append("| Metric | Class Average |")
        report.append("|--------|--------------|")
        report.append(f"| Overall Score | {overall_score_avg:.1f}% |")
        report.append(f"| Progress Score | {progress_score_avg:.1f}% |")
        report.append(f"| Engagement Score | {engagement_score_avg:.1f}% |")
        report.append(f"| Labs Completion Rate | {labs_completion_avg:.1f}% |")
        report.append(f"| Assessments Completion Rate | {assessments_completion_avg:.1f}% |")
        report.append(f"| Assessment Average Score | {assessments_score_avg:.1f}% |")
        report.append("")
        
        # Add student rankings section
        report.append("## Student Rankings")
        report.append("")
        report.append("### Overall Score")
        report.append("")
        report.append("| Rank | Student | Overall Score | Progress Score | Engagement Score |")
        report.append("|------|---------|--------------|----------------|------------------|")
        
        # Sort students by overall score
        students_by_overall = sorted(
            [(name, data) for name, data in self.metrics_data.items()],
            key=lambda x: x[1]['summary']['overall_score'],
            reverse=True
        )
        
        for i, (name, data) in enumerate(students_by_overall, 1):
            report.append(f"| {i} | {name} | {data['summary']['overall_score']:.1f}% | {data['summary']['progress_score']:.1f}% | {data['summary']['engagement_score']:.1f}% |")
        
        report.append("")
        
        # Add module progress section
        report.append("## Module Progress")
        report.append("")
        
        # Calculate module averages
        module_averages = {}
        for module_num in range(1, 15):
            module_labs_completion = []
            module_assessments_completion = []
            module_assessments_score = []
            
            for name, data in self.metrics_data.items():
                # Check if the module exists as either integer or string key
                module_key = None
                if module_num in data['modules']:
                    module_key = module_num
                elif str(module_num) in data['modules']:
                    module_key = str(module_num)
                
                if module_key is not None:
                    module_data = data['modules'][module_key]
                    if module_data['labs_total'] > 0:
                        module_labs_completion.append(module_data['labs_completion_rate'])
                    if module_data['assessments_total'] > 0:
                        module_assessments_completion.append(module_data['assessments_completion_rate'])
                        module_assessments_score.append(module_data['assessments_avg_score'])
            
            if module_labs_completion or module_assessments_completion:
                module_averages[module_num] = {
                    'labs_completion_avg': sum(module_labs_completion) / len(module_labs_completion) if module_labs_completion else 0,
                    'assessments_completion_avg': sum(module_assessments_completion) / len(module_assessments_completion) if module_assessments_completion else 0,
                    'assessments_score_avg': sum(module_assessments_score) / len(module_assessments_score) if module_assessments_score else 0
                }
        
        report.append("| Module | Labs Completion % | Assessment Avg. Score | Assessment Completion % |")
        report.append("|--------|-------------------|------------------------|-------------------------|")
        
        for module_num in sorted(module_averages.keys()):
            avg_data = module_averages[module_num]
            report.append(f"| Module {module_num} | {avg_data['labs_completion_avg']:.1f}% | {avg_data['assessments_score_avg']:.1f}% | {avg_data['assessments_completion_avg']:.1f}% |")
        
        report.append("")
        
        return "\n".join(report)

def main():
    """
    Main function to parse command line arguments and execute the report formatter.
    """
    parser = argparse.ArgumentParser(description='Format metrics data into markdown reports.')
    parser.add_argument('--metrics-file', required=True, help='Path to the combined metrics JSON file')
    parser.add_argument('--output-dir', default="reports", help='Directory to save the formatted reports')
    parser.add_argument('--student', help='Generate report for a specific student')
    parser.add_argument('--class-summary', action='store_true', help='Generate class summary report')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Create report formatter
    formatter = ReportFormatter(args.metrics_file)
    
    # Generate reports
    if args.student:
        # Create student reports directory
        student_reports_dir = os.path.join(args.output_dir, "student_reports")
        os.makedirs(student_reports_dir, exist_ok=True)
        
        report = formatter.format_student_report(args.student)
        output_path = os.path.join(student_reports_dir, f"{args.student.replace(' ', '_')}_report.md")
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"Student report saved to: {output_path}")
    
    if args.class_summary:
        # Create class summary directory
        class_summary_dir = os.path.join(args.output_dir, "class_summaries")
        os.makedirs(class_summary_dir, exist_ok=True)
        
        report = formatter.format_class_summary_report()
        output_path = os.path.join(class_summary_dir, "class_summary_report.md")
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"Class summary report saved to: {output_path}")
    
    if not args.student and not args.class_summary:
        print("No reports generated. Specify --student or --class-summary.")

if __name__ == "__main__":
    main()