#!/usr/bin/env python3
"""
Teaching Assistant Tool

This script provides interactive analysis and insights for teaching assistants
based on student data in JSON format. It helps identify students who need attention,
tracks progress, and provides recommendations for interventions.
"""

import argparse
import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple
import datetime
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

# Import functions from generate_reports.py
from generate_reports import (
    load_json_data, 
    extract_module_number,
    get_module_resources,
    count_completed_resources,
    format_time
)

class TeachingAssistant:
    def __init__(self, assessment_data_path: str, resource_time_data_path: str, study_history_data_path: str):
        """Initialize the Teaching Assistant with data paths."""
        self.assessment_data = load_json_data(assessment_data_path)
        self.resource_time_data = load_json_data(resource_time_data_path)
        self.study_history_data = load_json_data(study_history_data_path)
        self.current_module = 6  # Default to module 6
        
    def identify_at_risk_students(self, threshold_percentage: float = 30.0) -> List[Dict[str, Any]]:
        """
        Identify students who are at risk based on completion percentage.
        
        Args:
            threshold_percentage: Percentage below which students are considered at risk
            
        Returns:
            List of at-risk students with their stats
        """
        at_risk_students = []
        
        for student in self.assessment_data['students']:
            # Calculate completion percentage
            total_labs = len(student['labs'])
            completed_labs = count_completed_resources(student['labs'])
            completion_percentage = (completed_labs / total_labs * 100) if total_labs > 0 else 0
            
            # Calculate average assessment score
            total_score = sum(a['completion'] for a in student['assessments'])
            avg_assessment_score = (total_score / len(student['assessments'])) * 100 if student['assessments'] else 0
            
            # Check if student is at risk
            if completion_percentage < threshold_percentage:
                # Get study time data
                study_time = 0
                for student_data in self.study_history_data['students']:
                    if student_data['name'] == student['name']:
                        if 'total_study_time_seconds' in student_data:
                            study_time = student_data['total_study_time_seconds']
                        else:
                            study_time = sum([day['total_study_time_seconds'] for day in student_data['daily_study_time']])
                        break
                
                # Add to at-risk list
                at_risk_students.append({
                    'name': student['name'],
                    'email': student['email'],
                    'completion_percentage': completion_percentage,
                    'labs_completed': completed_labs,
                    'total_labs': total_labs,
                    'assessment_score': avg_assessment_score,
                    'study_time_hours': study_time / 3600,
                    'labs_behind': total_labs - completed_labs
                })
        
        # Sort by completion percentage (ascending)
        at_risk_students.sort(key=lambda x: x['completion_percentage'])
        
        return at_risk_students
    
    def get_module_progress(self, module_number: int) -> Dict[str, Any]:
        """
        Get detailed progress for a specific module.
        
        Args:
            module_number: Module number to analyze
            
        Returns:
            Dictionary with module statistics
        """
        module_stats = {
            'module_number': module_number,
            'students': [],
            'average_completion': 0,
            'average_time_spent': 0,
            'average_assessment_score': 0
        }
        
        total_completion = 0
        total_time_spent = 0
        total_assessment_score = 0
        student_count = 0
        
        for student in self.assessment_data['students']:
            # Get module labs
            module_labs = get_module_resources(student['labs'], module_number)
            total_module_labs = len(module_labs)
            
            if total_module_labs == 0:
                continue  # Skip if no labs for this module
                
            completed_module_labs = count_completed_resources(module_labs)
            completion_percentage = (completed_module_labs / total_module_labs * 100) if total_module_labs > 0 else 0
            
            # Get module assessments
            module_assessments = get_module_resources(student['assessments'], module_number)
            assessment_score = 0
            if module_assessments:
                assessment_score = sum(a['completion'] for a in module_assessments) / len(module_assessments) * 100
            
            # Get time spent
            time_spent = 0
            for student_data in self.resource_time_data['students']:
                if student_data['name'] == student['name']:
                    # Check if resources is a dictionary with categories or a list
                    if isinstance(student_data['resources'], dict):
                        # Handle nested structure with categories
                        for resource_type, resources in student_data['resources'].items():
                            if resource_type in ['lab', 'assessment', 'fact_sheet']:
                                for resource in resources:
                                    if isinstance(resource, dict) and 'name' in resource:
                                        resource_module = extract_module_number(resource['name'])
                                        if resource_module == module_number:
                                            time_spent += resource.get('time_seconds', 0)
                    else:
                        # Handle flat list of resources
                        for resource in student_data['resources']:
                            if isinstance(resource, dict) and 'name' in resource:
                                resource_module = extract_module_number(resource['name'])
                                if resource_module == module_number:
                                    time_spent += resource.get('time_spent_seconds', 0)
            
            # Add to module stats
            module_stats['students'].append({
                'name': student['name'],
                'email': student['email'],
                'labs_completed': completed_module_labs,
                'total_labs': total_module_labs,
                'completion_percentage': completion_percentage,
                'assessment_score': assessment_score,
                'time_spent_seconds': time_spent,
                'time_spent_formatted': format_time(time_spent)
            })
            
            total_completion += completion_percentage
            total_time_spent += time_spent
            total_assessment_score += assessment_score
            student_count += 1
        
        # Calculate averages
        if student_count > 0:
            module_stats['average_completion'] = total_completion / student_count
            module_stats['average_time_spent'] = total_time_spent / student_count
            module_stats['average_assessment_score'] = total_assessment_score / student_count
        
        # Sort by completion percentage (descending)
        module_stats['students'].sort(key=lambda x: x['completion_percentage'], reverse=True)
        
        return module_stats
    
    def get_student_insights(self, student_name: str) -> Dict[str, Any]:
        """
        Get detailed insights for a specific student.
        
        Args:
            student_name: Name of the student to analyze
            
        Returns:
            Dictionary with student insights
        """
        # Find student in assessment data
        student_data = None
        for student in self.assessment_data['students']:
            if student['name'] == student_name:
                student_data = student
                break
        
        if not student_data:
            return {'error': f'Student {student_name} not found'}
        
        # Get study history
        study_history = None
        for student in self.study_history_data['students']:
            if student['name'] == student_name:
                study_history = student
                break
        
        # Get resource time
        resource_time = None
        for student in self.resource_time_data['students']:
            if student['name'] == student_name:
                resource_time = student
                break
        
        # Calculate overall stats
        total_labs = len(student_data['labs'])
        completed_labs = count_completed_resources(student_data['labs'])
        completion_percentage = (completed_labs / total_labs * 100) if total_labs > 0 else 0
        
        # Calculate assessment stats
        total_score = sum(a['completion'] for a in student_data['assessments'])
        avg_assessment_score = (total_score / len(student_data['assessments'])) * 100 if student_data['assessments'] else 0
        
        # Calculate module-specific stats
        module_stats = []
        for module in range(1, self.current_module + 1):
            module_labs = get_module_resources(student_data['labs'], module)
            total_module_labs = len(module_labs)
            completed_module_labs = count_completed_resources(module_labs)
            module_completion = (completed_module_labs / total_module_labs * 100) if total_module_labs > 0 else 0
            
            # Get module assessments
            module_assessments = get_module_resources(student_data['assessments'], module)
            assessment_score = 0
            if module_assessments:
                assessment_score = sum(a['completion'] for a in module_assessments) / len(module_assessments) * 100
            
            # Get time spent
            time_spent = 0
            if resource_time:
                # Check if resources is a dictionary with categories or a list
                if isinstance(resource_time['resources'], dict):
                    # Handle nested structure with categories
                    for resource_type, resources in resource_time['resources'].items():
                        if resource_type in ['lab', 'assessment', 'fact_sheet']:
                            for resource in resources:
                                if isinstance(resource, dict) and 'name' in resource:
                                    resource_module = extract_module_number(resource['name'])
                                    if resource_module == module:
                                        time_spent += resource.get('time_seconds', 0)
                else:
                    # Handle flat list of resources
                    for resource in resource_time['resources']:
                        if isinstance(resource, dict) and 'name' in resource:
                            resource_module = extract_module_number(resource['name'])
                            if resource_module == module:
                                time_spent += resource.get('time_spent_seconds', 0)
            
            module_stats.append({
                'module': module,
                'labs_completed': completed_module_labs,
                'total_labs': total_module_labs,
                'completion_percentage': module_completion,
                'assessment_score': assessment_score,
                'time_spent_seconds': time_spent,
                'time_spent_formatted': format_time(time_spent)
            })
        
        # Calculate study patterns
        study_patterns = []
        if study_history:
            # Check if daily_study_time is a dictionary or a list
            if 'daily_study' in study_history:
                # Handle list of daily study entries
                for day_entry in study_history['daily_study']:
                    if day_entry['study_time_seconds'] > 0:
                        study_patterns.append({
                            'date': day_entry['date'],
                            'time_spent_seconds': day_entry['study_time_seconds'],
                            'time_spent_formatted': day_entry['study_time_formatted'] or format_time(day_entry['study_time_seconds'])
                        })
            elif 'daily_study_time' in study_history and isinstance(study_history['daily_study_time'], dict):
                # Handle dictionary of date -> time
                for date, time_spent in study_history['daily_study_time'].items():
                    if isinstance(time_spent, str):
                        # Convert time string to seconds
                        hours, minutes, seconds = 0, 0, 0
                        time_parts = time_spent.split()
                        for part in time_parts:
                            if 'h' in part:
                                hours = int(part.replace('h', ''))
                            elif 'm' in part:
                                minutes = int(part.replace('m', ''))
                            elif 's' in part:
                                seconds = int(part.replace('s', ''))
                        time_seconds = hours * 3600 + minutes * 60 + seconds
                    else:
                        time_seconds = time_spent
                    
                    if time_seconds > 0:
                        study_patterns.append({
                            'date': date,
                            'time_spent_seconds': time_seconds,
                            'time_spent_formatted': format_time(time_seconds)
                        })
        
        # Sort study patterns by date
        study_patterns.sort(key=lambda x: x['date'])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            student_data, 
            module_stats, 
            total_completion=completion_percentage, 
            assessment_scores=avg_assessment_score, 
            study_patterns=study_patterns
        )
        
        return {
            'name': student_name,
            'email': student_data['email'],
            'overall_completion': completion_percentage,
            'labs_completed': completed_labs,
            'total_labs': total_labs,
            'average_assessment_score': avg_assessment_score,
            'module_stats': module_stats,
            'study_patterns': study_patterns,
            'recommendations': recommendations
        }
    
    def _generate_recommendations(
        self, 
        student_data: Dict[str, Any], 
        module_stats: List[Dict[str, Any]],
        total_completion: float,
        assessment_scores: float,
        study_patterns: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate personalized recommendations for a student."""
        recommendations = []
        
        # Check for module completion (more important than overall completion)
        completed_modules = sum(1 for m in module_stats if m['completion_percentage'] == 100)
        total_modules = len(module_stats)
        module_completion_rate = (completed_modules / total_modules) * 100 if total_modules > 0 else 0
        
        # Use module completion rate as primary indicator
        if module_completion_rate >= 80:
            # Student is doing well on modules
            recommendations.append("Student is making excellent progress through the modules.")
        elif module_completion_rate >= 50:
            recommendations.append("Student is making good progress but could benefit from completing older modules.")
        elif total_completion < 30:
            recommendations.append("URGENT: Completion rate is very low. Schedule a one-on-one meeting to identify barriers.")
        elif total_completion < 60:
            recommendations.append("Completion rate is below average. Encourage more consistent progress through the labs.")
        
        # Check for low assessment scores
        avg_assessment = assessment_scores
        if avg_assessment >= 70:
            recommendations.append("Assessment scores are strong. Consider offering additional challenges.")
        elif avg_assessment < 20:
            recommendations.append("Assessment scores are very low. Review fundamental concepts and provide additional resources.")
        elif avg_assessment < 50:
            recommendations.append("Assessment scores need improvement. Suggest focused review of key topics.")
        
        # Check for study patterns
        if study_patterns:
            try:
                # Try to parse dates in different formats
                dates = []
                for p in study_patterns:
                    try:
                        # Try YYYY-MM-DD format
                        date = datetime.datetime.strptime(p['date'], '%Y-%m-%d')
                    except ValueError:
                        try:
                            # Try Month DD, Day format (e.g., "Apr 15, Tuesday")
                            date = datetime.datetime.strptime(p['date'].split(',')[0], '%b %d')
                            # Set year to current year since it's missing
                            date = date.replace(year=datetime.datetime.now().year)
                        except ValueError:
                            # If all else fails, just use today's date
                            date = datetime.datetime.now()
                    dates.append(date)
                
                if dates:
                    # Sort dates
                    dates.sort()
                    
                    # Check for recent activity
                    last_study = dates[-1]
                    today = datetime.datetime.now()
                    days_since_last_study = (today - last_study).days
                    
                    if days_since_last_study > 14:
                        recommendations.append(f"No study activity for {days_since_last_study} days. Reach out to check on student status.")
                    elif days_since_last_study > 7:
                        recommendations.append(f"Limited recent activity ({days_since_last_study} days since last study). Encourage more regular engagement.")
                    
                    # Check for study consistency
                    if len(dates) >= 3:
                        date_diffs = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
                        avg_days_between = sum(date_diffs) / len(date_diffs) if date_diffs else 0
                        
                        if avg_days_between > 5:
                            recommendations.append(f"Inconsistent study pattern (avg {avg_days_between:.1f} days between sessions). Suggest more regular schedule.")
                        else:
                            recommendations.append("Good study consistency. Encourage maintaining this pattern.")
            except Exception as e:
                # If there's any error in date processing, add a generic recommendation
                recommendations.append("Review study patterns to ensure regular engagement with course materials.")
        else:
            recommendations.append("No study history available. Encourage student to log into the platform regularly.")
        
        # Module-specific recommendations
        incomplete_modules = [m for m in module_stats if m['completion_percentage'] < 100]
        if incomplete_modules:
            lowest_module = min(incomplete_modules, key=lambda x: x['completion_percentage'])
            recommendations.append(f"Focus on completing Module {lowest_module['module']} labs (currently at {lowest_module['completion_percentage']:.1f}% completion).")
        
        return recommendations
    
    def visualize_class_progress(self, output_path: str) -> None:
        """
        Generate visualizations of class progress and save to file.
        
        Args:
            output_path: Path to save the visualization
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("Required packages not found. Installing matplotlib...")
            import subprocess
            subprocess.check_call(["uv", "pip", "install", "matplotlib"])
            import matplotlib.pyplot as plt
            import numpy as np
        
        # Create figure with multiple subplots
        fig = plt.figure(figsize=(15, 10))
        fig.suptitle('Class Progress Overview', fontsize=16)
        
        # 1. Overall completion by student
        ax1 = fig.add_subplot(221)
        student_names = []
        completion_percentages = []
        
        for student in self.assessment_data['students']:
            total_labs = len(student['labs'])
            completed_labs = count_completed_resources(student['labs'])
            completion_percentage = (completed_labs / total_labs * 100) if total_labs > 0 else 0
            
            student_names.append(student['name'].split(',')[0])  # Just use last name
            completion_percentages.append(completion_percentage)
        
        # Sort by completion percentage
        sorted_indices = np.argsort(completion_percentages)
        sorted_names = [student_names[i] for i in sorted_indices]
        sorted_percentages = [completion_percentages[i] for i in sorted_indices]
        
        bars = ax1.barh(sorted_names[-10:], sorted_percentages[-10:], color='skyblue')
        ax1.set_xlabel('Completion Percentage')
        ax1.set_title('Top 10 Students by Completion')
        ax1.set_xlim(0, 100)
        
        # Add percentage labels
        for bar, percentage in zip(bars, sorted_percentages[-10:]):
            ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                    f'{percentage:.1f}%', va='center')
        
        # 2. Module completion across class
        ax2 = fig.add_subplot(222)
        module_completions = []
        module_numbers = list(range(1, self.current_module + 1))
        
        for module in module_numbers:
            module_stats = self.get_module_progress(module)
            module_completions.append(module_stats['average_completion'])
        
        ax2.bar(module_numbers, module_completions, color='lightgreen')
        ax2.set_xlabel('Module')
        ax2.set_ylabel('Average Completion Percentage')
        ax2.set_title('Average Module Completion')
        ax2.set_ylim(0, 100)
        
        # Add percentage labels
        for i, v in enumerate(module_completions):
            ax2.text(i + 1, v + 1, f'{v:.1f}%', ha='center')
        
        # 3. Assessment scores vs. lab completion
        ax3 = fig.add_subplot(223)
        assessment_scores = []
        
        for student in self.assessment_data['students']:
            total_labs = len(student['labs'])
            completed_labs = count_completed_resources(student['labs'])
            completion_percentage = (completed_labs / total_labs * 100) if total_labs > 0 else 0
            
            total_score = sum(a['completion'] for a in student['assessments'])
            avg_assessment_score = (total_score / len(student['assessments'])) * 100 if student['assessments'] else 0
            
            assessment_scores.append(avg_assessment_score)
        
        ax3.scatter(completion_percentages, assessment_scores, alpha=0.7)
        ax3.set_xlabel('Lab Completion Percentage')
        ax3.set_ylabel('Assessment Score')
        ax3.set_title('Assessment Score vs. Lab Completion')
        ax3.set_xlim(0, 100)
        ax3.set_ylim(0, 100)
        
        # Add trend line
        z = np.polyfit(completion_percentages, assessment_scores, 1)
        p = np.poly1d(z)
        ax3.plot(sorted(completion_percentages), p(sorted(completion_percentages)), "r--", alpha=0.7)
        
        # 4. Time spent vs. completion
        ax4 = fig.add_subplot(224)
        time_spent = []
        
        for student in self.assessment_data['students']:
            # Find student in resource time data
            student_time = 0
            for s in self.resource_time_data['students']:
                if s['name'] == student['name']:
                    student_time = sum(r['time_spent_seconds'] for r in s['resources'])
                    break
            
            time_spent.append(student_time / 3600)  # Convert to hours
        
        ax4.scatter(time_spent, completion_percentages, alpha=0.7)
        ax4.set_xlabel('Time Spent (hours)')
        ax4.set_ylabel('Completion Percentage')
        ax4.set_title('Completion vs. Time Spent')
        
        # Add trend line
        z = np.polyfit(time_spent, completion_percentages, 1)
        p = np.poly1d(z)
        ax4.plot(sorted(time_spent), p(sorted(time_spent)), "r--", alpha=0.7)
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(output_path)
        print(f"Visualization saved to {output_path}")
    
    def print_at_risk_students(self, threshold_percentage: float = 30.0) -> None:
        """Print a table of at-risk students."""
        try:
            from tabulate import tabulate
        except ImportError:
            print("Required package not found. Installing tabulate...")
            import subprocess
            subprocess.check_call(["uv", "pip", "install", "tabulate"])
            from tabulate import tabulate
            
        at_risk_students = self.identify_at_risk_students(threshold_percentage)
        
        if not at_risk_students:
            print(f"No students below the {threshold_percentage}% completion threshold.")
            return
        
        table_data = []
        for student in at_risk_students:
            table_data.append([
                student['name'],
                student['email'],
                f"{student['completion_percentage']:.1f}%",
                f"{student['labs_completed']}/{student['total_labs']}",
                f"{student['assessment_score']:.1f}%",
                f"{student['study_time_hours']:.1f} hours",
                student['labs_behind']
            ])
        
        headers = ["Name", "Email", "Completion", "Labs", "Assessment", "Study Time", "Labs Behind"]
        print("\n=== STUDENTS AT RISK ===")
        print(f"Threshold: Below {threshold_percentage}% completion")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def print_module_progress(self, module_number: int) -> None:
        """Print detailed progress for a specific module."""
        try:
            from tabulate import tabulate
        except ImportError:
            print("Required package not found. Installing tabulate...")
            import subprocess
            subprocess.check_call(["uv", "pip", "install", "tabulate"])
            from tabulate import tabulate
            
        module_stats = self.get_module_progress(module_number)
        
        print(f"\n=== MODULE {module_number} PROGRESS ===")
        print(f"Average Completion: {module_stats['average_completion']:.1f}%")
        print(f"Average Time Spent: {format_time(module_stats['average_time_spent'])}")
        print(f"Average Assessment Score: {module_stats['average_assessment_score']:.1f}%")
        
        table_data = []
        for student in module_stats['students']:
            table_data.append([
                student['name'],
                f"{student['labs_completed']}/{student['total_labs']}",
                f"{student['completion_percentage']:.1f}%",
                student['time_spent_formatted'],
                f"{student['assessment_score']:.1f}%"
            ])
        
        headers = ["Name", "Labs", "Completion", "Time Spent", "Assessment"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def print_student_insights(self, student_name: str) -> None:
        """Print detailed insights for a specific student."""
        try:
            from tabulate import tabulate
        except ImportError:
            print("Required package not found. Installing tabulate...")
            import subprocess
            subprocess.check_call(["uv", "pip", "install", "tabulate"])
            from tabulate import tabulate
            
        insights = self.get_student_insights(student_name)
        
        if 'error' in insights:
            print(insights['error'])
            return
        
        print(f"\n=== STUDENT INSIGHTS: {insights['name']} ===")
        print(f"Email: {insights['email']}")
        print(f"Overall Completion: {insights['overall_completion']:.1f}%")
        print(f"Labs Completed: {insights['labs_completed']}/{insights['total_labs']}")
        print(f"Average Assessment Score: {insights['average_assessment_score']:.1f}%")
        
        print("\nModule Progress:")
        module_table = []
        for module in insights['module_stats']:
            module_table.append([
                module['module'],
                f"{module['labs_completed']}/{module['total_labs']}",
                f"{module['completion_percentage']:.1f}%",
                module['time_spent_formatted'],
                f"{module['assessment_score']:.1f}%"
            ])
        
        headers = ["Module", "Labs", "Completion", "Time Spent", "Assessment"]
        print(tabulate(module_table, headers=headers, tablefmt="grid"))
        
        if insights['study_patterns']:
            print("\nRecent Study Activity:")
            study_table = []
            for pattern in insights['study_patterns'][-5:]:  # Show last 5 days
                study_table.append([
                    pattern['date'],
                    pattern['time_spent_formatted']
                ])
            
            headers = ["Date", "Time Spent"]
            print(tabulate(study_table, headers=headers, tablefmt="simple"))
        
        print("\nRecommendations:")
        for i, recommendation in enumerate(insights['recommendations'], 1):
            print(f"{i}. {recommendation}")

def main():
    """Main function to parse command line arguments and execute the teaching assistant."""
    parser = argparse.ArgumentParser(description='Teaching Assistant Tool')
    parser.add_argument('--assessment-data', 
                        help='Path to the assessment data JSON file')
    parser.add_argument('--resource-time-data', 
                        help='Path to the resource time data JSON file')
    parser.add_argument('--study-history-data', 
                        help='Path to the study history data JSON file')
    parser.add_argument('--date', 
                        help='Date folder to use (format: YY-MM-DD)')
    parser.add_argument('--at-risk', action='store_true',
                        help='List students at risk')
    parser.add_argument('--threshold', type=float, default=30.0,
                        help='Completion percentage threshold for at-risk students')
    parser.add_argument('--module', type=int,
                        help='Module number to analyze')
    parser.add_argument('--student',
                        help='Student name to analyze')
    parser.add_argument('--visualize', action='store_true',
                        help='Generate visualizations of class progress')
    parser.add_argument('--output',
                        help='Path to save the visualization')
    
    args = parser.parse_args()
    
    # Handle date-based directory structure
    if args.date:
        date_folder = args.date
    else:
        # Find the latest date folder
        processed_dirs = [d for d in os.listdir(os.path.join("assets", "processed")) 
                         if os.path.isdir(os.path.join("assets", "processed", d))]
        if not processed_dirs:
            print("No processed data folders found.")
            return
        date_folder = sorted(processed_dirs)[-1]  # Get the latest date
        print(f"Using latest date folder: {date_folder}")
    
    # Set up paths based on date folder
    processed_date_dir = os.path.join("assets", "processed", date_folder)
    reports_date_dir = os.path.join("reports", date_folder)
    
    # Ensure reports directory exists
    os.makedirs(reports_date_dir, exist_ok=True)
    
    # Find the assessment data file
    if args.assessment_data:
        assessment_data_path = args.assessment_data
    else:
        # Find the latest classgradebook file in the date folder
        assessment_files = [f for f in os.listdir(processed_date_dir) 
                          if f.startswith("classgradebook") and f.endswith(".json")]
        if not assessment_files:
            print(f"No assessment data files found in {processed_date_dir}")
            return
        assessment_data_path = os.path.join(processed_date_dir, assessment_files[0])
        print(f"Using assessment data: {assessment_data_path}")
    
    # Find the resource time data file
    if args.resource_time_data:
        resource_time_data_path = args.resource_time_data
    else:
        # Find the latest timeperresource file in the date folder
        resource_time_files = [f for f in os.listdir(processed_date_dir) 
                             if f.startswith("timeperresource") and f.endswith(".json")]
        if not resource_time_files:
            print(f"No resource time data files found in {processed_date_dir}")
            return
        resource_time_data_path = os.path.join(processed_date_dir, resource_time_files[0])
        print(f"Using resource time data: {resource_time_data_path}")
    
    # Find the study history data file
    if args.study_history_data:
        study_history_data_path = args.study_history_data
    else:
        # Find the latest classstudyhistory file in the date folder
        study_history_files = [f for f in os.listdir(processed_date_dir) 
                              if f.startswith("classstudyhistory") and f.endswith(".json")]
        if not study_history_files:
            print(f"No study history data files found in {processed_date_dir}")
            return
        study_history_data_path = os.path.join(processed_date_dir, study_history_files[0])
        print(f"Using study history data: {study_history_data_path}")
    
    # Set default output path if not specified
    if args.visualize and not args.output:
        args.output = os.path.join(reports_date_dir, "class_visualization.png")
        print(f"Visualization will be saved to: {args.output}")
    
    # Create teaching assistant
    ta = TeachingAssistant(
        assessment_data_path,
        resource_time_data_path,
        study_history_data_path
    )
    
    # Process commands
    if args.at_risk:
        ta.print_at_risk_students(args.threshold)
    
    if args.module:
        ta.print_module_progress(args.module)
    
    if args.student:
        ta.print_student_insights(args.student)
    
    if args.visualize:
        ta.visualize_class_progress(args.output)
    
    # If no specific command is given, show help
    if not (args.at_risk or args.module or args.student or args.visualize):
        parser.print_help()

if __name__ == "__main__":
    main()
