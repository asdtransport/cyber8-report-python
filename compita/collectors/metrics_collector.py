#!/usr/bin/env python3
"""
Metrics Collector

This script collects and combines metrics from all three flexible reports:
1. Module completion data (flexible_module_report)
2. Study time data (flexible_assessment_report)
3. Assessment grades data (flexible_grades_report)

It generates comprehensive metrics per student, per module range, and per week,
creating a unified dataset that can be used for progress reports.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import argparse
import re

class MetricsCollector:
    """
    A class to collect and process metrics from multiple data sources.
    """
    
    def __init__(self, date_folder, output_prefix="combined_metrics"):
        """
        Initialize the MetricsCollector with the specified date folder.
        
        Args:
            date_folder (str): The date folder to process (format: YY-MM-DD)
            output_prefix (str): Prefix for the output files
        """
        self.date_folder = date_folder
        self.output_prefix = output_prefix
        self.processed_dir = os.path.join("assets", "processed", date_folder)
        self.reports_dir = os.path.join("reports", date_folder)
        self.metrics_dir = os.path.join(self.reports_dir, "metrics")
        
        # Create metrics directory if it doesn't exist
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        # Initialize data containers
        self.module_data = None
        self.study_data = None
        self.grades_data = None
        self.combined_metrics = {}
        self.weekly_metrics = {}
        self.module_range_metrics = {}
        
        # Load the latest data files
        self._load_latest_data()
    
    def _load_latest_data(self):
        """
        Load the latest data from the processed directory.
        """
        # Find the latest classgradebook JSON file
        gradebook_files = [f for f in os.listdir(self.processed_dir) if f.startswith("classgradebook") and f.endswith(".json")]
        if gradebook_files:
            gradebook_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.processed_dir, x)), reverse=True)
            self.gradebook_file = os.path.join(self.processed_dir, gradebook_files[0])
            print(f"Using gradebook data from: {self.gradebook_file}")
            
            # Load the gradebook data
            with open(self.gradebook_file, 'r') as f:
                self.gradebook_data = json.load(f)
        else:
            print(f"Warning: No classgradebook JSON files found in {self.processed_dir}")
            self.gradebook_data = {"students": []}
        
        # Find the latest classstudyhistory JSON file
        studyhistory_files = [f for f in os.listdir(self.processed_dir) if (f.startswith("classstudyhistory") or f.startswith("studyhistory")) and f.endswith(".json")]
        if studyhistory_files:
            studyhistory_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.processed_dir, x)), reverse=True)
            self.studyhistory_file = os.path.join(self.processed_dir, studyhistory_files[0])
            print(f"Using study history data from: {self.studyhistory_file}")
            
            # Load the study history data
            with open(self.studyhistory_file, 'r') as f:
                self.studyhistory_data = json.load(f)
        else:
            print(f"Warning: No classstudyhistory JSON files found in {self.processed_dir}")
            self.studyhistory_data = {"students": []}
    
    def collect_module_metrics(self):
        """
        Collect metrics from the module completion data.
        """
        print("Collecting module completion metrics...")
        
        # Initialize module metrics for each student
        for student in self.gradebook_data.get("students", []):
            student_name = student.get("name", "").strip()  # Strip whitespace from student names
            student_email = student.get("email", "")
            
            if student_name not in self.combined_metrics:
                self.combined_metrics[student_name] = {
                    "email": student_email,
                    "modules": {},
                    "assessments": {},
                    "study_time": {},
                    "weekly_metrics": {},
                    "summary": {}
                }
            
            # Process labs for each module
            for lab in student.get("labs", []):
                lab_name = lab.get("name", "")
                completion = lab.get("completion", 0)
                
                # Extract module number using regex
                module_match = re.search(r'Lab - (\d+)\.', lab_name)
                if module_match:
                    module_num = int(module_match.group(1))
                    
                    # Initialize module data if not already present
                    if module_num not in self.combined_metrics[student_name]["modules"]:
                        self.combined_metrics[student_name]["modules"][module_num] = {
                            "labs_completed": 0,
                            "labs_total": 0,
                            "labs_completion_rate": 0,
                            "assessments_completed": 0,
                            "assessments_total": 0,
                            "assessments_avg_score": 0,
                            "assessments_completion_rate": 0
                        }
                    
                    # Count this lab for the module
                    self.combined_metrics[student_name]["modules"][module_num]["labs_total"] += 1
                    
                    # Check if the lab is completed
                    if completion == 1.0:
                        self.combined_metrics[student_name]["modules"][module_num]["labs_completed"] += 1
        
        # Calculate completion rates for each module
        for student_name, data in self.combined_metrics.items():
            for module_num, module_data in data["modules"].items():
                if module_data["labs_total"] > 0:
                    module_data["labs_completion_rate"] = (module_data["labs_completed"] / module_data["labs_total"]) * 100
                else:
                    module_data["labs_completion_rate"] = 0
        
        print("Module completion metrics collected.")
    
    def collect_assessment_metrics(self):
        """
        Collect metrics from the assessment grades data.
        """
        print("Collecting assessment grade metrics...")
        
        # Initialize assessment metrics for each student
        for student in self.gradebook_data.get("students", []):
            student_name = student.get("name", "").strip()  # Strip whitespace from student names
            
            if student_name not in self.combined_metrics:
                continue  # Skip if student not in combined_metrics (should not happen)
            
            # Process assessments for each module
            for assessment in student.get("assessments", []):
                assessment_name = assessment.get("name", "")
                completion = assessment.get("completion", 0)
                
                # Skip if assessment name is invalid
                if not assessment_name.startswith("Assessment -"):
                    continue
                
                # Extract module number and assessment type using regex
                module_match = re.search(r'Assessment - (\d+)\.(\d+)(?:\.(\d+))? (.+)', assessment_name)
                if module_match:
                    module_num = int(module_match.group(1))
                    assessment_type = module_match.group(4)
                    
                    # Initialize module data if not already present
                    if module_num not in self.combined_metrics[student_name]["modules"]:
                        self.combined_metrics[student_name]["modules"][module_num] = {
                            "labs_completed": 0,
                            "labs_total": 0,
                            "labs_completion_rate": 0,
                            "assessments_completed": 0,
                            "assessments_total": 0,
                            "assessments_avg_score": 0,
                            "assessments_completion_rate": 0
                        }
                    
                    # Initialize assessment type data if not already present
                    if assessment_type not in self.combined_metrics[student_name]["assessments"]:
                        self.combined_metrics[student_name]["assessments"][assessment_type] = {
                            "completed": 0,
                            "total": 0,
                            "avg_score": 0,
                            "completion_rate": 0
                        }
                    
                    # Count this assessment for the module and type
                    self.combined_metrics[student_name]["modules"][module_num]["assessments_total"] += 1
                    self.combined_metrics[student_name]["assessments"][assessment_type]["total"] += 1
                    
                    # Add to the total score
                    self.combined_metrics[student_name]["modules"][module_num]["assessments_avg_score"] += completion
                    self.combined_metrics[student_name]["assessments"][assessment_type]["avg_score"] += completion
                    
                    # Check if the assessment is completed (using 0.7 as threshold)
                    if completion >= 0.7:
                        self.combined_metrics[student_name]["modules"][module_num]["assessments_completed"] += 1
                        self.combined_metrics[student_name]["assessments"][assessment_type]["completed"] += 1
        
        # Calculate average scores and completion rates
        for student_name, data in self.combined_metrics.items():
            # For modules
            for module_num, module_data in data["modules"].items():
                if module_data["assessments_total"] > 0:
                    module_data["assessments_avg_score"] = (module_data["assessments_avg_score"] / module_data["assessments_total"]) * 100
                    module_data["assessments_completion_rate"] = (module_data["assessments_completed"] / module_data["assessments_total"]) * 100
                else:
                    module_data["assessments_avg_score"] = 0
                    module_data["assessments_completion_rate"] = 0
            
            # For assessment types
            for assessment_type, type_data in data["assessments"].items():
                if type_data["total"] > 0:
                    type_data["avg_score"] = (type_data["avg_score"] / type_data["total"]) * 100
                    type_data["completion_rate"] = (type_data["completed"] / type_data["total"]) * 100
                else:
                    type_data["avg_score"] = 0
                    type_data["completion_rate"] = 0
        
        print("Assessment grade metrics collected.")
    
    def collect_study_time_metrics(self):
        """
        Collect metrics from the study time data.
        """
        print("Collecting study time metrics...")
        
        # Initialize study time metrics for each student
        for student in self.studyhistory_data.get("students", []):
            student_name = student.get("name", "").strip()  # Strip whitespace from student names
            
            # Initialize student data if not already present
            if student_name not in self.combined_metrics:
                self.combined_metrics[student_name] = {
                    "email": student.get("email", ""),
                    "modules": {},
                    "assessments": {},
                    "study_time": {},
                    "weekly_metrics": {},
                    "summary": {}
                }
            
            # Get total study time
            total_study_time = student.get("total_study_time_seconds", 0)
            study_days = student.get("study_days", 0)
            avg_daily_study_time = student.get("average_daily_study_time_seconds", 0)
            
            # Store study time summary
            self.combined_metrics[student_name]["study_time"]["total_seconds"] = total_study_time
            self.combined_metrics[student_name]["study_time"]["study_days"] = study_days
            self.combined_metrics[student_name]["study_time"]["avg_daily_seconds"] = avg_daily_study_time
            self.combined_metrics[student_name]["study_time"]["total_formatted"] = self._format_time(total_study_time)
            self.combined_metrics[student_name]["study_time"]["avg_daily_formatted"] = self._format_time(avg_daily_study_time)
            
            # Process daily study data
            for daily in student.get("daily_study", []):
                date_str = daily.get("date", "")
                study_time_seconds = daily.get("study_time_seconds", 0)
                
                # Skip if date is empty or invalid
                if not date_str:
                    continue
                
                # Extract week number
                week_num = self._get_week_number(date_str)
                
                # Initialize week data if not already present
                if week_num not in self.combined_metrics[student_name]["weekly_metrics"]:
                    self.combined_metrics[student_name]["weekly_metrics"][week_num] = {
                        "study_time_seconds": 0,
                        "study_days": 0,
                        "labs_completed": 0,
                        "assessments_completed": 0
                    }
                
                # Add study time for this day
                self.combined_metrics[student_name]["weekly_metrics"][week_num]["study_time_seconds"] += study_time_seconds
                
                # Count as a study day if time > 0
                if study_time_seconds > 0:
                    self.combined_metrics[student_name]["weekly_metrics"][week_num]["study_days"] += 1
        
        # Format study time for each week
        for student_name, data in self.combined_metrics.items():
            for week_num, week_data in data["weekly_metrics"].items():
                week_data["study_time_formatted"] = self._format_time(week_data["study_time_seconds"])
        
        print("Study time metrics collected.")
    
    def calculate_summary_metrics(self):
        """
        Calculate summary metrics for each student.
        """
        print("Calculating summary metrics...")
        
        for student_name, data in self.combined_metrics.items():
            # Initialize summary metrics
            total_labs_completed = 0
            total_labs = 0
            total_assessments_completed = 0
            total_assessments = 0
            total_assessment_score = 0
            
            # Sum up module metrics
            for module_num, module_data in data["modules"].items():
                total_labs_completed += module_data["labs_completed"]
                total_labs += module_data["labs_total"]
                total_assessments_completed += module_data["assessments_completed"]
                total_assessments += module_data["assessments_total"]
                total_assessment_score += module_data["assessments_avg_score"] * module_data["assessments_total"]
            
            # Calculate overall metrics
            data["summary"]["total_labs_completed"] = total_labs_completed
            data["summary"]["total_labs"] = total_labs
            data["summary"]["total_assessments_completed"] = total_assessments_completed
            data["summary"]["total_assessments"] = total_assessments
            
            # Calculate completion rates
            if total_labs > 0:
                data["summary"]["labs_completion_rate"] = (total_labs_completed / total_labs) * 100
            else:
                data["summary"]["labs_completion_rate"] = 0
            
            if total_assessments > 0:
                data["summary"]["assessments_completion_rate"] = (total_assessments_completed / total_assessments) * 100
                data["summary"]["assessments_avg_score"] = total_assessment_score / total_assessments
            else:
                data["summary"]["assessments_completion_rate"] = 0
                data["summary"]["assessments_avg_score"] = 0
            
            # Calculate combined progress score (weighted average of labs and assessments)
            if total_labs > 0 and total_assessments > 0:
                lab_weight = 0.6  # 60% weight to labs
                assessment_weight = 0.4  # 40% weight to assessments
                
                data["summary"]["progress_score"] = (
                    (data["summary"]["labs_completion_rate"] * lab_weight) +
                    (data["summary"]["assessments_completion_rate"] * assessment_weight)
                )
            elif total_labs > 0:
                data["summary"]["progress_score"] = data["summary"]["labs_completion_rate"]
            elif total_assessments > 0:
                data["summary"]["progress_score"] = data["summary"]["assessments_completion_rate"]
            else:
                data["summary"]["progress_score"] = 0
            
            # Calculate engagement score based on study time and activity
            study_time_score = min(100, (data["study_time"].get("total_seconds", 0) / 3600) / 40 * 100)  # 40 hours = 100%
            study_days_score = min(100, (data["study_time"].get("study_days", 0) / 20) * 100)  # 20 days = 100%
            
            data["summary"]["engagement_score"] = (study_time_score * 0.7) + (study_days_score * 0.3)
            
            # Calculate overall score (progress + engagement)
            data["summary"]["overall_score"] = (data["summary"]["progress_score"] * 0.7) + (data["summary"]["engagement_score"] * 0.3)
        
        print("Summary metrics calculated.")
    
    def calculate_module_range_metrics(self):
        """
        Calculate metrics for different module ranges.
        """
        print("Calculating module range metrics...")
        
        # Define module ranges
        module_ranges = {
            "early": list(range(1, 6)),  # Modules 1-5
            "middle": list(range(6, 11)),  # Modules 6-10
            "late": list(range(11, 15))  # Modules 11-14
        }
        
        # Initialize module range metrics for each student
        for student_name, data in self.combined_metrics.items():
            data["module_ranges"] = {}
            
            for range_name, modules in module_ranges.items():
                data["module_ranges"][range_name] = {
                    "modules": modules,
                    "labs_completed": 0,
                    "labs_total": 0,
                    "labs_completion_rate": 0,
                    "assessments_completed": 0,
                    "assessments_total": 0,
                    "assessments_avg_score": 0,
                    "assessments_completion_rate": 0
                }
                
                # Sum up metrics for modules in this range
                total_assessment_score = 0
                for module_num in modules:
                    if module_num in data["modules"]:
                        module_data = data["modules"][module_num]
                        data["module_ranges"][range_name]["labs_completed"] += module_data["labs_completed"]
                        data["module_ranges"][range_name]["labs_total"] += module_data["labs_total"]
                        data["module_ranges"][range_name]["assessments_completed"] += module_data["assessments_completed"]
                        data["module_ranges"][range_name]["assessments_total"] += module_data["assessments_total"]
                        total_assessment_score += module_data["assessments_avg_score"] * module_data["assessments_total"]
                
                # Calculate completion rates
                if data["module_ranges"][range_name]["labs_total"] > 0:
                    data["module_ranges"][range_name]["labs_completion_rate"] = (
                        data["module_ranges"][range_name]["labs_completed"] / 
                        data["module_ranges"][range_name]["labs_total"]
                    ) * 100
                else:
                    data["module_ranges"][range_name]["labs_completion_rate"] = 0
                
                if data["module_ranges"][range_name]["assessments_total"] > 0:
                    data["module_ranges"][range_name]["assessments_completion_rate"] = (
                        data["module_ranges"][range_name]["assessments_completed"] / 
                        data["module_ranges"][range_name]["assessments_total"]
                    ) * 100
                    data["module_ranges"][range_name]["assessments_avg_score"] = (
                        total_assessment_score / data["module_ranges"][range_name]["assessments_total"]
                    )
                else:
                    data["module_ranges"][range_name]["assessments_completion_rate"] = 0
                    data["module_ranges"][range_name]["assessments_avg_score"] = 0
        
        print("Module range metrics calculated.")
    
    def collect_all_metrics(self):
        """
        Collect all metrics and save the results.
        """
        self.collect_module_metrics()
        self.collect_assessment_metrics()
        self.collect_study_time_metrics()
        self.calculate_summary_metrics()
        self.calculate_module_range_metrics()
        
        # Save the combined metrics to a JSON file
        output_path = os.path.join(self.metrics_dir, f"{self.output_prefix}.json")
        with open(output_path, 'w') as f:
            json.dump(self.combined_metrics, f, indent=2)
        
        print(f"Combined metrics saved to: {output_path}")
        
        return output_path
    
    def _format_time(self, seconds):
        """
        Format seconds into a human-readable string (e.g., "5h 30m 15s").
        
        Args:
            seconds (float): Time in seconds
        
        Returns:
            str: Formatted time string
        """
        if seconds == 0:
            return "0s"
        
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def _get_week_number(self, date_str):
        """
        Get the week number for a date string.
        
        Args:
            date_str (str): Date string in format "MMM D, Day" (e.g., "Apr 15, Tuesday")
        
        Returns:
            int: Week number (1-based)
        """
        # Extract month and day from the date string
        date_parts = date_str.split(',')[0].strip().split(' ')
        if len(date_parts) != 2:
            return 1  # Default to week 1 if format is invalid
        
        month, day = date_parts
        day = int(day)
        
        # Convert month names to numbers
        month_to_num = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        
        month_num = month_to_num.get(month, 1)
        
        # Use April 15 as the start of week 1
        base_month = 4  # April
        base_day = 15
        
        # Create date objects for comparison
        current_year = datetime.now().year
        date_obj = datetime(current_year, month_num, day)
        base_date = datetime(current_year, base_month, base_day)
        
        # Calculate days since base date
        if date_obj < base_date:
            # For dates before April 15, treat them as part of the first 3 weeks
            # Calculate days before base date
            days_before_base = (base_date - date_obj).days
            # Map to weeks 1-3 based on proximity to base date
            if days_before_base <= 7:
                return 1  # Within 1 week before base date
            elif days_before_base <= 14:
                return 2  # Within 2 weeks before base date
            else:
                return 3  # More than 2 weeks before base date
        else:
            # For dates on or after April 15, calculate week number normally
            days_since_base = (date_obj - base_date).days
            week_num = (days_since_base // 7) + 1
            return week_num

def main():
    """
    Main function to parse command line arguments and execute the metrics collector.
    """
    parser = argparse.ArgumentParser(description='Collect and combine metrics from all flexible reports.')
    parser.add_argument('--date', required=True, help='Date folder to process (format: YY-MM-DD)')
    parser.add_argument('--output-prefix', default="combined_metrics", help='Prefix for the output files')
    
    args = parser.parse_args()
    
    # Create metrics collector and collect all metrics
    collector = MetricsCollector(args.date, args.output_prefix)
    output_path = collector.collect_all_metrics()
    
    print(f"Metrics collection complete!")
    print(f"Combined metrics saved to: {output_path}")

if __name__ == "__main__":
    main()

# Add adapter function for the new CLI interface
def collect_metrics(date):
    """
    Collect and combine metrics from all data sources.
    
    Args:
        date (str): Date in YY-MM-DD format
        
    Returns:
        dict: Combined metrics
    """
    collector = MetricsCollector(date)
    return collector.collect_all_metrics()
