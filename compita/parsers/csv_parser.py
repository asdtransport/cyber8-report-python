#!/usr/bin/env python3
"""
Unified CSV to JSON Parser for Student Data
This script parses various CSV files containing student data and converts them to JSON format,
organizing the data by students and different metrics (assessments, study time, resource time).
"""

import os
import json
import argparse
import re
import glob
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

try:
    import pandas as pd
except ImportError:
    print("Error: The pandas library is required for CSV parsing.")
    print("Please install it using: pip3 install pandas")
    print("Or install the complete package with: pip3 install -e .")
    pd = None

# Utility functions for time parsing (used by resource_time and study_history parsers)
def parse_time_string(time_str: str) -> int:
    """
    Parse a time string in the format "Xh Ym Zs" to total seconds.
    
    Args:
        time_str: Time string in the format "Xh Ym Zs"
        
    Returns:
        Total seconds as an integer
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    if pd.isna(time_str) or time_str == "":
        return 0
        
    total_seconds = 0
    
    # Handle hours
    if "h" in time_str:
        hours_part = time_str.split("h")[0].split()[-1]
        total_seconds += int(hours_part) * 3600
        time_str = time_str.split("h")[1].strip()
    
    # Handle minutes
    if "m" in time_str:
        minutes_part = time_str.split("m")[0].split()[-1]
        total_seconds += int(minutes_part) * 60
        time_str = time_str.split("m")[1].strip()
    
    # Handle seconds
    if "s" in time_str:
        seconds_part = time_str.split("s")[0].split()[-1]
        total_seconds += int(seconds_part)
    
    return total_seconds

def format_seconds_to_time(seconds: int) -> str:
    """
    Format seconds to a time string in the format "Xh Ym Zs".
    
    Args:
        seconds: Total seconds
        
    Returns:
        Formatted time string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    result = ""
    if hours > 0:
        result += f"{hours}h "
    if minutes > 0 or hours > 0:
        result += f"{minutes}m "
    result += f"{secs}s"
    
    return result.strip()

# Categorization functions for different parsers
def categorize_column(column_name: str) -> str:
    """
    Categorize a column name into one of the assessment types.
    
    Args:
        column_name: The name of the column from the CSV file
        
    Returns:
        The category type (assessment, lab, lesson, fact_sheet, video)
    """
    column_lower = column_name.lower()
    
    if "assessment" in column_lower:
        return "assessment"
    elif "lab" in column_lower:
        return "lab"
    elif "lesson" in column_lower:
        return "lesson"
    elif "fact sheet" in column_lower:
        return "fact_sheet"
    elif "video" in column_lower:
        return "video"
    else:
        return "other"

def categorize_resource(resource_name: str) -> str:
    """
    Categorize a resource name into one of the resource types.
    
    Args:
        resource_name: The name of the resource from the CSV file
        
    Returns:
        The category type (fact_sheet, assessment, lab, etc.)
    """
    return categorize_column(resource_name)  # Same logic for both functions

# Directory and file utility functions
def find_latest_date_folder(base_dir: str) -> Optional[str]:
    """
    Find the latest date folder in the base directory.
    
    Args:
        base_dir: Base directory containing date folders
        
    Returns:
        Path to the latest date folder or None if no folders found
    """
    date_pattern = re.compile(r'^\d{2}-\d{2}-\d{2}$')
    
    # Get all directories in the base directory
    date_dirs = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and date_pattern.match(item):
            date_dirs.append(item)
    
    if not date_dirs:
        return None
    
    # Sort directories by date (assuming format is YY-MM-DD)
    date_dirs.sort(reverse=True)
    
    return os.path.join(base_dir, date_dirs[0])

def find_csv_files(directory: str, file_type: str = None) -> List[str]:
    """
    Find all CSV files in a directory that match the specified type.
    
    Args:
        directory: Directory to search for CSV files
        file_type: Type of CSV file to find (e.g., 'classgradebook', 'timeperresource')
        
    Returns:
        List of paths to CSV files
    """
    if file_type:
        pattern = os.path.join(directory, f"*{file_type}*.csv")
    else:
        pattern = os.path.join(directory, "*.csv")
    
    return glob.glob(pattern)

def extract_date_time_from_filename(filename: str) -> Tuple[str, str]:
    """
    Extract date and time information from a filename.
    
    Args:
        filename: Filename to extract date and time from
        
    Returns:
        Tuple of (date, time) strings
    """
    # Extract date (format: MM-DD)
    date_match = re.search(r'(\d{1,2}-\d{1,2})', filename)
    date = date_match.group(1) if date_match else "unknown"
    
    # Extract time (format: [N]am/pm)
    time_match = re.search(r'(\d{1,2}(?:am|pm))', filename)
    time = time_match.group(1) if time_match else "unknown"
    
    return date, time

def ensure_output_dir(date_folder: str, output_dir: str) -> str:
    """
    Ensure the output directory exists for the specified date folder.
    
    Args:
        date_folder: Date folder name (format: YY-MM-DD)
        output_dir: Output directory
        
    Returns:
        Path to the output directory
    """
    output_dir_path = os.path.join(output_dir, date_folder)
    
    # Check if the path exists but is a file
    if os.path.exists(output_dir_path) and not os.path.isdir(output_dir_path):
        # Rename the file to avoid conflicts
        os.rename(output_dir_path, f"{output_dir_path}_file")
        print(f"Warning: {output_dir_path} existed as a file and was renamed to {output_dir_path}_file")
    
    # Create the directory
    os.makedirs(output_dir_path, exist_ok=True)
    return output_dir_path

# Main parser functions for different file types
def parse_csv_to_json(csv_file_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Parse a CSV file containing student assessment data and convert it to JSON format.
    
    Args:
        csv_file_path: Path to the CSV file
        output_dir: Directory to save the JSON output
        
    Returns:
        A dictionary containing the parsed data
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Initialize the result dictionary
    result = {
        "students": [],
        "metadata": {
            "total_students": 0,
            "assessment_types": {
                "assessment": 0,
                "lab": 0,
                "lesson": 0,
                "fact_sheet": 0,
                "video": 0,
                "other": 0
            }
        }
    }
    
    # Count assessment types
    assessment_counts = {
        "assessment": 0,
        "lab": 0,
        "lesson": 0,
        "fact_sheet": 0,
        "video": 0,
        "other": 0
    }
    
    # Process each column and categorize it
    column_categories = {}
    for column in df.columns[1:]:  # Skip the first column (Student)
        category = categorize_column(column)
        column_categories[column] = category
        assessment_counts[category] += 1
    
    # Update metadata
    result["metadata"]["assessment_types"] = assessment_counts
    
    # Process each student
    for _, row in df.iterrows():
        student_name = row["Student"]
        
        # Skip empty rows
        if pd.isna(student_name) or student_name.strip() == "":
            continue
            
        # Extract email from student name if available
        email = ""
        if "(" in student_name and ")" in student_name:
            email = student_name.split("(")[1].split(")")[0]
            student_name = student_name.split("(")[0].strip()
        
        # Initialize student data
        student_data = {
            "name": student_name,
            "email": email,
            "assessments": [],
            "labs": [],
            "lessons": [],
            "fact_sheets": [],
            "videos": [],
            "other": [],
            "summary": {
                "total_completed": 0,
                "total_items": 0,
                "completion_percentage": 0
            }
        }
        
        # Process each assessment for this student
        total_completed = 0
        total_items = 0
        
        for column in df.columns[1:]:  # Skip the first column (Student)
            value = row[column]
            
            # Skip if value is NaN
            if pd.isna(value):
                continue
                
            # Convert percentage string to float
            if isinstance(value, str) and "%" in value:
                completion = float(value.strip("%")) / 100
            else:
                try:
                    completion = float(value) / 100
                except (ValueError, TypeError):
                    completion = 0
            
            # Create assessment item
            assessment_item = {
                "name": column,
                "completion": completion
            }
            
            # Add to appropriate category
            category = column_categories[column]
            if category == "assessment":
                student_data["assessments"].append(assessment_item)
            elif category == "lab":
                student_data["labs"].append(assessment_item)
            elif category == "lesson":
                student_data["lessons"].append(assessment_item)
            elif category == "fact_sheet":
                student_data["fact_sheets"].append(assessment_item)
            elif category == "video":
                student_data["videos"].append(assessment_item)
            else:
                student_data["other"].append(assessment_item)
            
            # Update completion statistics
            total_items += 1
            total_completed += completion
        
        # Calculate completion percentage
        if total_items > 0:
            completion_percentage = (total_completed / total_items)
        else:
            completion_percentage = 0
        
        # Update summary
        student_data["summary"]["total_completed"] = total_completed
        student_data["summary"]["total_items"] = total_items
        student_data["summary"]["completion_percentage"] = completion_percentage
        
        # Add student to result
        result["students"].append(student_data)
    
    # Update total students count
    result["metadata"]["total_students"] = len(result["students"])
    
    # Save to JSON
    date_match = re.search(r'(\d{2}-\d{2}-\d{2})', csv_file_path)
    if date_match:
        date_dir = date_match.group(1)
        output_dir_path = ensure_output_dir(date_dir, output_dir)
        output_file = os.path.join(output_dir_path, 'classgradebook.json')
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"JSON data written to {output_file}")
    
    return result

def parse_resource_time_to_json(csv_file_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Parse a CSV file containing time spent per resource by students and convert it to JSON format.
    
    Args:
        csv_file_path: Path to the CSV file
        output_dir: Directory to save the JSON output
        
    Returns:
        A dictionary containing the parsed data
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Initialize the result dictionary
    result = {
        "students": [],
        "metadata": {
            "total_students": 0,
            "resource_types": {
                "assessment": {
                    "count": 0,
                    "total_time_seconds": 0,
                    "total_time_formatted": ""
                },
                "lab": {
                    "count": 0,
                    "total_time_seconds": 0,
                    "total_time_formatted": ""
                },
                "lesson": {
                    "count": 0,
                    "total_time_seconds": 0,
                    "total_time_formatted": ""
                },
                "fact_sheet": {
                    "count": 0,
                    "total_time_seconds": 0,
                    "total_time_formatted": ""
                },
                "video": {
                    "count": 0,
                    "total_time_seconds": 0,
                    "total_time_formatted": ""
                },
                "other": {
                    "count": 0,
                    "total_time_seconds": 0,
                    "total_time_formatted": ""
                }
            },
            "total_resources": 0,
            "class_total_time_seconds": 0,
            "class_total_time_formatted": ""
        }
    }
    
    # Count resource types
    resource_counts = {
        "assessment": 0,
        "lab": 0,
        "lesson": 0,
        "fact_sheet": 0,
        "video": 0,
        "other": 0
    }
    
    # Process each column and categorize it
    resource_categories = {}
    for column in df.columns[1:]:  # Skip the first column (Student)
        category = categorize_resource(column)
        resource_categories[column] = category
        resource_counts[category] += 1
    
    # Update metadata
    for category, count in resource_counts.items():
        result["metadata"]["resource_types"][category]["count"] = count
    
    result["metadata"]["total_resources"] = sum(resource_counts.values())
    
    # Process each student
    class_total_seconds = 0
    
    for _, row in df.iterrows():
        student_name = row["Student"]
        
        # Skip empty rows
        if pd.isna(student_name) or student_name.strip() == "":
            continue
            
        # Extract email from student name if available
        email = ""
        if "(" in student_name and ")" in student_name:
            email = student_name.split("(")[1].split(")")[0]
            student_name = student_name.split("(")[0].strip()
        
        # Initialize student data
        student_data = {
            "name": student_name,
            "email": email,
            "resources": {
                "assessment": [],
                "lab": [],
                "fact_sheet": [],
                "lesson": [],
                "video": [],
                "other": []
            },
            "summary": {
                "total_time_seconds": 0,
                "total_time_formatted": "",
                "resource_type_summary": {
                    "assessment": {
                        "count": 0,
                        "total_time_seconds": 0,
                        "total_time_formatted": "",
                        "average_time_seconds": 0,
                        "average_time_formatted": ""
                    },
                    "lab": {
                        "count": 0,
                        "total_time_seconds": 0,
                        "total_time_formatted": "",
                        "average_time_seconds": 0,
                        "average_time_formatted": ""
                    },
                    "lesson": {
                        "count": 0,
                        "total_time_seconds": 0,
                        "total_time_formatted": "",
                        "average_time_seconds": 0,
                        "average_time_formatted": ""
                    },
                    "fact_sheet": {
                        "count": 0,
                        "total_time_seconds": 0,
                        "total_time_formatted": "",
                        "average_time_seconds": 0,
                        "average_time_formatted": ""
                    },
                    "video": {
                        "count": 0,
                        "total_time_seconds": 0,
                        "total_time_formatted": "",
                        "average_time_seconds": 0,
                        "average_time_formatted": ""
                    },
                    "other": {
                        "count": 0,
                        "total_time_seconds": 0,
                        "total_time_formatted": "",
                        "average_time_seconds": 0,
                        "average_time_formatted": ""
                    }
                }
            }
        }
        
        # Initialize counters for resource types
        type_counts = {
            "assessment": 0,
            "lab": 0,
            "lesson": 0,
            "fact_sheet": 0,
            "video": 0,
            "other": 0
        }
        
        type_seconds = {
            "assessment": 0,
            "lab": 0,
            "lesson": 0,
            "fact_sheet": 0,
            "video": 0,
            "other": 0
        }
        
        # Process each resource for this student
        total_seconds = 0
        
        for column in df.columns[1:]:  # Skip the first column (Student)
            time_str = row[column]
            
            # Skip if value is NaN or empty
            if pd.isna(time_str) or time_str == "":
                continue
                
            # Parse time string to seconds
            seconds = parse_time_string(time_str)
            
            # Skip if no time spent
            if seconds == 0:
                continue
                
            # Get resource category
            category = resource_categories[column]
            
            # Create resource item
            resource_item = {
                "name": column,
                "time_seconds": seconds,
                "time_formatted": time_str
            }
            
            # Add to appropriate category
            student_data["resources"][category].append(resource_item)
            
            # Update counters
            type_counts[category] += 1
            type_seconds[category] += seconds
            total_seconds += seconds
        
        # Update student summary
        student_data["summary"]["total_time_seconds"] = total_seconds
        student_data["summary"]["total_time_formatted"] = format_seconds_to_time(total_seconds)
        
        # Update resource type summaries
        for category in type_counts.keys():
            count = type_counts[category]
            seconds = type_seconds[category]
            
            student_data["summary"]["resource_type_summary"][category]["count"] = count
            student_data["summary"]["resource_type_summary"][category]["total_time_seconds"] = seconds
            student_data["summary"]["resource_type_summary"][category]["total_time_formatted"] = format_seconds_to_time(seconds)
            
            # Calculate average time per resource type
            if count > 0:
                avg_seconds = seconds // count
                student_data["summary"]["resource_type_summary"][category]["average_time_seconds"] = avg_seconds
                student_data["summary"]["resource_type_summary"][category]["average_time_formatted"] = format_seconds_to_time(avg_seconds)
        
        # Add student to result
        result["students"].append(student_data)
        
        # Update class total time
        class_total_seconds += total_seconds
        
        # Update class resource type totals
        for category, seconds in type_seconds.items():
            result["metadata"]["resource_types"][category]["total_time_seconds"] += seconds
    
    # Update metadata
    result["metadata"]["total_students"] = len(result["students"])
    result["metadata"]["class_total_time_seconds"] = class_total_seconds
    result["metadata"]["class_total_time_formatted"] = format_seconds_to_time(class_total_seconds)
    
    # Format resource type total times
    for category in result["metadata"]["resource_types"].keys():
        seconds = result["metadata"]["resource_types"][category]["total_time_seconds"]
        result["metadata"]["resource_types"][category]["total_time_formatted"] = format_seconds_to_time(seconds)
    
    # Save to JSON
    date_match = re.search(r'(\d{2}-\d{2}-\d{2})', csv_file_path)
    if date_match:
        date_dir = date_match.group(1)
        output_dir_path = ensure_output_dir(date_dir, output_dir)
        output_file = os.path.join(output_dir_path, 'timeperresource.json')
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"JSON data written to {output_file}")
    
    return result

def parse_study_history_to_json(csv_file_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Parse a CSV file containing student study history data and convert it to JSON format.
    
    Args:
        csv_file_path: Path to the CSV file
        output_dir: Directory to save the JSON output
        
    Returns:
        A dictionary containing the parsed data
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Initialize the result dictionary
    result = {
        "students": [],
        "metadata": {
            "total_students": 0,
            "date_range": {
                "start_date": "",
                "end_date": ""
            },
            "total_study_days": 0,
            "class_total_study_time_seconds": 0
        }
    }
    
    # Extract date range
    date_columns = df.columns[2:]  # Skip 'Student' and 'Total Time Spent'
    if len(date_columns) > 0:
        result["metadata"]["date_range"]["start_date"] = date_columns[0]
        result["metadata"]["date_range"]["end_date"] = date_columns[-1]
        result["metadata"]["total_study_days"] = len(date_columns)
    
    # Process each student
    class_total_seconds = 0
    
    for _, row in df.iterrows():
        student_name = row["Student"]
        
        # Skip empty rows
        if pd.isna(student_name) or student_name.strip() == "":
            continue
            
        # Extract email from student name if available
        email = ""
        if "(" in student_name and ")" in student_name:
            email = student_name.split("(")[1].split(")")[0]
            student_name = student_name.split("(")[0].strip()
        
        # Parse total time spent
        total_time_str = row["Total Time Spent"]
        total_seconds = parse_time_string(total_time_str)
        class_total_seconds += total_seconds
        
        # Initialize student data
        student_data = {
            "name": student_name,
            "email": email,
            "total_study_time_seconds": total_seconds,
            "total_study_time_formatted": format_seconds_to_time(total_seconds),
            "daily_study": [],
            "study_days": 0,
            "average_daily_study_time_seconds": 0,
            "average_daily_study_time_formatted": ""
        }
        
        # Process each day for this student
        study_days = 0
        
        for day_column in date_columns:
            day_time_str = row[day_column]
            
            # Parse time for this day
            if pd.isna(day_time_str) or day_time_str == "":
                day_seconds = 0
            else:
                day_seconds = parse_time_string(day_time_str)
                if day_seconds > 0:
                    study_days += 1
            
            # Create day entry
            day_entry = {
                "date": day_column,
                "study_time_seconds": day_seconds,
                "study_time_formatted": format_seconds_to_time(day_seconds) if day_seconds > 0 else ""
            }
            
            student_data["daily_study"].append(day_entry)
        
        # Calculate average daily study time (only for days with study activity)
        student_data["study_days"] = study_days
        if study_days > 0:
            avg_daily_seconds = total_seconds // study_days
            student_data["average_daily_study_time_seconds"] = avg_daily_seconds
            student_data["average_daily_study_time_formatted"] = format_seconds_to_time(avg_daily_seconds)
        
        # Add student to result
        result["students"].append(student_data)
    
    # Update metadata
    result["metadata"]["total_students"] = len(result["students"])
    result["metadata"]["class_total_study_time_seconds"] = class_total_seconds
    result["metadata"]["class_total_study_time_formatted"] = format_seconds_to_time(class_total_seconds)
    
    # Calculate class average study time
    if result["metadata"]["total_students"] > 0:
        class_avg_seconds = class_total_seconds // result["metadata"]["total_students"]
        result["metadata"]["class_average_study_time_seconds"] = class_avg_seconds
        result["metadata"]["class_average_study_time_formatted"] = format_seconds_to_time(class_avg_seconds)
    
    # Save to JSON
    date_match = re.search(r'(\d{2}-\d{2}-\d{2})', csv_file_path)
    if date_match:
        date_dir = date_match.group(1)
        output_dir_path = ensure_output_dir(date_dir, output_dir)
        output_file = os.path.join(output_dir_path, 'studyhistory.json')
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"JSON data written to {output_file}")
    
    return result

def process_latest_csv(base_dir: str, file_type: str = None, output_dir: str = None) -> Optional[Dict[str, Any]]:
    """
    Process the latest CSV file of the specified type.
    
    Args:
        base_dir: Base directory containing date folders
        file_type: Type of CSV file to process (e.g., 'classgradebook', 'timeperresource')
        output_dir: Directory to save the JSON output
        
    Returns:
        Dictionary containing the parsed data or None if no CSV files found
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    # Find the latest date folder
    latest_date_folder = find_latest_date_folder(base_dir)
    if not latest_date_folder:
        print(f"No date folders found in {base_dir}")
        return None
    
    # Find CSV files in the latest date folder
    csv_files = find_csv_files(latest_date_folder, file_type)
    if not csv_files:
        print(f"No CSV files found in {latest_date_folder}")
        return None
    
    # Sort CSV files by modification time (latest first)
    csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_csv = csv_files[0]
    
    # Parse the CSV file
    print(f"Processing {latest_csv}")
    if file_type == 'timeperresource':
        result = parse_resource_time_to_json(latest_csv, output_dir)
    elif file_type == 'studyhistory':
        result = parse_study_history_to_json(latest_csv, output_dir)
    else:
        result = parse_csv_to_json(latest_csv, output_dir)
    
    return result

def process_specific_date_csv(base_dir: str, date_folder: str, file_type: str = None, output_dir: str = None) -> Optional[Dict[str, Any]]:
    """
    Process a CSV file from a specific date folder.
    
    Args:
        base_dir (str): Base directory containing date folders
        date_folder (str): Date folder to process
        file_type (str, optional): Type of CSV file to process. Defaults to None.
        output_dir (str, optional): Output directory for JSON files. Defaults to None.
        
    Returns:
        Optional[Dict[str, Any]]: Processed data, or None if no CSV file found
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    date_path = os.path.join(base_dir, date_folder)
    if not os.path.exists(date_path):
        print(f"Date folder not found: {date_path}")
        return None
    
    csv_files = find_csv_files(date_path, file_type)
    if not csv_files:
        print(f"No {file_type} CSV files found in {date_path}")
        return None
    
    # Sort by modification time (newest first)
    csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    csv_file = csv_files[0]
    print(f"Processing {csv_file}")
    
    # Process the CSV file based on its type
    if file_type == 'classgradebook':
        data = parse_csv_to_json(csv_file, output_dir)
    elif file_type == 'studyhistory':
        data = parse_study_history_to_json(csv_file, output_dir)
    elif file_type == 'timeperresource':
        data = parse_resource_time_to_json(csv_file, output_dir)
    else:
        print(f"Unknown file type: {file_type}")
        return None
    
    # Skip saving the standard filename JSON file since we'll save with the original filename in parse_csv
    
    return data

def process_all_date_folders(base_dir: str, file_type: str = None, output_dir: str = None) -> Dict[str, Dict[str, Any]]:
    """
    Process CSV files from all date folders.
    
    Args:
        base_dir: Base directory containing date folders
        file_type: Type of CSV file to process (e.g., 'classgradebook', 'timeperresource')
        output_dir: Directory to save the JSON output
        
    Returns:
        Dictionary mapping date folders to parsed data
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    date_pattern = re.compile(r'^\d{2}-\d{2}-\d{2}$')
    
    # Get all date directories in the base directory
    date_dirs = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and date_pattern.match(item):
            date_dirs.append(item)
    
    if not date_dirs:
        print(f"No date folders found in {base_dir}")
        return {}
    
    # Sort directories by date (assuming format is YY-MM-DD)
    date_dirs.sort(reverse=True)
    
    # Process each date folder
    results = {}
    for date_dir in date_dirs:
        date_path = os.path.join(base_dir, date_dir)
        
        # Find CSV files in the date folder
        csv_files = find_csv_files(date_path, file_type)
        if not csv_files:
            print(f"No CSV files found in {date_path}")
            continue
        
        # Sort CSV files by modification time (latest first)
        csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        latest_csv = csv_files[0]
        
        # Parse the CSV file
        print(f"Processing {latest_csv}")
        if file_type == 'timeperresource':
            result = parse_resource_time_to_json(latest_csv, output_dir)
        elif file_type == 'studyhistory':
            result = parse_study_history_to_json(latest_csv, output_dir)
        else:
            result = parse_csv_to_json(latest_csv, output_dir)
        
        results[date_dir] = result
    
    return results

def main():
    """Main function to parse command line arguments and execute the parser."""
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    parser = argparse.ArgumentParser(description='Parse CSV files containing student data to JSON format.')
    parser.add_argument('--csv_file', help='Path to a specific CSV file (optional)')
    parser.add_argument('--base_dir', help='Base directory containing date folders (default: assets/comptia)', 
                        default='assets/comptia')
    parser.add_argument('--date', help='Specific date folder to process (format: YY-MM-DD)')
    parser.add_argument('--file_type', choices=['classgradebook', 'timeperresource', 'studyhistory'], 
                        help='Type of CSV file to process (classgradebook, timeperresource, studyhistory)')
    parser.add_argument('--all_dates', action='store_true', help='Process all date folders')
    parser.add_argument('-o', '--output', help='Directory to save the JSON output (optional)')
    parser.add_argument('--parser_type', choices=['gradebook', 'resource', 'study'], 
                        help='Type of parser to use (gradebook, resource, study)')
    
    args = parser.parse_args()
    
    # Determine parser type from file_type if not explicitly specified
    if not args.parser_type and args.file_type:
        if args.file_type == 'classgradebook':
            args.parser_type = 'gradebook'
        elif args.file_type == 'timeperresource':
            args.parser_type = 'resource'
        elif args.file_type == 'studyhistory':
            args.parser_type = 'study'
    
    # Process a specific CSV file if provided
    if args.csv_file:
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            # Extract date from CSV file path if possible
            date_match = re.search(r'(\d{2}-\d{2}-\d{2})', args.csv_file)
            if date_match:
                date_folder = date_match.group(1)
            else:
                # Use current date in YY-MM-DD format if date not found in filename
                current_date = datetime.now().strftime("%y-%m-%d")
                date_folder = current_date
            
            # Create output directory in assets/processed/YY-MM-DD
            output_dir = ensure_output_dir(date_folder, args.output)
            base_name = os.path.splitext(os.path.basename(args.csv_file))[0]
            output_path = os.path.join(output_dir, f"{base_name}.json")
        
        # Choose parser based on file type or explicit parser type
        if args.parser_type == 'resource' or 'timeperresource' in args.csv_file:
            parse_resource_time_to_json(args.csv_file, output_path)
        elif args.parser_type == 'study' or 'studyhistory' in args.csv_file:
            parse_study_history_to_json(args.csv_file, output_path)
        else:
            parse_csv_to_json(args.csv_file, output_path)
    
    # Process all date folders
    elif args.all_dates:
        # Process each date folder
        date_pattern = re.compile(r'^\d{2}-\d{2}-\d{2}$')
        
        for item in os.listdir(args.base_dir):
            item_path = os.path.join(args.base_dir, item)
            if os.path.isdir(item_path) and date_pattern.match(item):
                date_dir = item
                
                # Create output directory in assets/processed/YY-MM-DD
                output_dir = ensure_output_dir(date_dir, args.output)
                
                # Process each file type
                if args.file_type:
                    # Process only the specified file type
                    process_specific_date_csv(args.base_dir, date_dir, args.file_type, output_dir)
                else:
                    # Process all file types
                    process_specific_date_csv(args.base_dir, date_dir, 'classgradebook', output_dir)
                    process_specific_date_csv(args.base_dir, date_dir, 'timeperresource', output_dir)
                    process_specific_date_csv(args.base_dir, date_dir, 'studyhistory', output_dir)
    
    # Process a specific date folder
    elif args.date:
        # Create output directory in assets/processed/YY-MM-DD
        output_dir = ensure_output_dir(args.date, args.output)
        
        # Process each file type
        if args.file_type:
            # Process only the specified file type
            process_specific_date_csv(args.base_dir, args.date, args.file_type, output_dir)
        else:
            # Process all file types
            process_specific_date_csv(args.base_dir, args.date, 'classgradebook', output_dir)
            process_specific_date_csv(args.base_dir, args.date, 'timeperresource', output_dir)
            process_specific_date_csv(args.base_dir, args.date, 'studyhistory', output_dir)
    
    # Process the latest date folder (default)
    else:
        # Find the latest date folder
        latest_date_folder = find_latest_date_folder(args.base_dir)
        if not latest_date_folder:
            print(f"No date folders found in {args.base_dir}")
            return
        
        # Extract just the folder name (YY-MM-DD) from the path
        date_folder = os.path.basename(latest_date_folder)
        
        # Create output directory in assets/processed/YY-MM-DD
        output_dir = ensure_output_dir(date_folder, args.output)
        
        # Process each file type
        if args.file_type:
            # Process only the specified file type
            process_latest_csv(args.base_dir, args.file_type, output_dir)
        else:
            # Process all file types
            process_latest_csv(args.base_dir, 'classgradebook', output_dir)
            process_latest_csv(args.base_dir, 'timeperresource', output_dir)
            process_latest_csv(args.base_dir, 'studyhistory', output_dir)

if __name__ == "__main__":
    main()

# Add adapter function for the new CLI interface
def parse_csv(date, file_type, parser_type, assets_dir='assets'):
    """
    Parse a CSV file and convert it to JSON.
    
    Args:
        date (str): Date in YY-MM-DD format
        file_type (str): Type of CSV file (classgradebook, studyhistory, timeperresource)
        parser_type (str): Type of parser to use (gradebook, study, resource)
        assets_dir (str): Path to the assets directory (default: 'assets')
        
    Returns:
        dict: Parsed data
    """
    if pd is None:
        raise ImportError("pandas is required for CSV parsing")
    base_dir = f'{assets_dir}/comptia'
    output_dir = f'{assets_dir}/processed/{date}'
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process the CSV file
    if parser_type == 'gradebook':
        data = process_specific_date_csv(base_dir, date, file_type, output_dir)
        if data:
            output_file = os.path.join(output_dir, 'assessment_data.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Saved assessment data to {output_file}")
            return data
    elif parser_type == 'resource':
        data = process_specific_date_csv(base_dir, date, file_type, output_dir)
        if data:
            output_file = os.path.join(output_dir, 'resource_time_data.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Saved resource time data to {output_file}")
            return data
    elif parser_type == 'study':
        data = process_specific_date_csv(base_dir, date, file_type, output_dir)
        if data:
            output_file = os.path.join(output_dir, 'study_history_data.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Saved study history data to {output_file}")
            return data
    
    return None
