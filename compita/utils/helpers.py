"""
Helper functions for the Cyber8 report generator.
"""
import os
import json
import datetime
from pathlib import Path

def format_time_seconds(seconds):
    """
    Format seconds into a human-readable string (e.g., "1h 30m 45s").
    
    Args:
        seconds (int): The number of seconds to format.
        
    Returns:
        str: A formatted time string.
    """
    if seconds is None or seconds == 0:
        return "0s"
    
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def ensure_directory(directory_path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path (str or Path): The path to the directory.
        
    Returns:
        Path: The path to the directory.
    """
    path = Path(directory_path)
    os.makedirs(path, exist_ok=True)
    return path

def ensure_dir_exists(directory_path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): Path to the directory to ensure exists
        
    Returns:
        str: The path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

def get_timestamp():
    """
    Get a formatted timestamp for use in filenames.
    
    Returns:
        str: A formatted timestamp.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def load_json(file_path):
    """
    Load JSON data from a file.
    
    Args:
        file_path (str or Path): The path to the JSON file.
        
    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """
    Save data to a JSON file.
    
    Args:
        data (dict): The data to save.
        file_path (str or Path): The path to the JSON file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def normalize_student_name(name):
    """
    Normalize a student name by stripping whitespace.
    
    Args:
        name (str): The student name to normalize.
        
    Returns:
        str: The normalized student name.
    """
    if not name:
        return name
    return name.strip()
