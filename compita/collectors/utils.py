"""
Utility functions for metrics collection.
"""
import os
import json
from datetime import datetime
from pathlib import Path

def load_json_data(file_path):
    """
    Load JSON data from a file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Loaded JSON data or empty dict if file not found
    """
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading JSON data from {file_path}: {e}")
        return {}

def save_json_data(data, file_path):
    """
    Save data to a JSON file.
    
    Args:
        data (dict): Data to save
        file_path (str): Path to the JSON file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving JSON data to {file_path}: {e}")
        return False

def get_week_number(date_str):
    """
    Calculate the week number for a given date string.
    
    Args:
        date_str (str): Date string in the format "MMM D, YYYY"
        
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

def normalize_student_name(name):
    """
    Normalize a student name by stripping whitespace.
    
    Args:
        name (str): Student name
        
    Returns:
        str: Normalized student name
    """
    return name.strip() if name else name
