"""
Utility functions for parsing CSV files.
"""
import os
import re
import glob
from datetime import datetime
from pathlib import Path

def find_latest_date_folder(base_dir):
    """
    Find the latest date folder in the base directory.
    
    Args:
        base_dir (str): Base directory containing date folders
        
    Returns:
        str: Path to the latest date folder or None if no folders found
    """
    # Get all date folders
    date_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    
    # Filter for date folders in YY-MM-DD format
    date_pattern = re.compile(r'^\d{2}-\d{2}-\d{2}$')
    date_folders = [f for f in date_folders if date_pattern.match(f)]
    
    if not date_folders:
        return None
    
    # Sort by date (newest first)
    date_folders.sort(key=lambda x: datetime.strptime(x, '%y-%m-%d'), reverse=True)
    
    return os.path.join(base_dir, date_folders[0])

def find_csv_files(directory, file_type=None):
    """
    Find all CSV files in a directory that match the specified type.
    
    Args:
        directory (str): Directory to search for CSV files
        file_type (str): Type of CSV file to find (e.g., 'classgradebook', 'timeperresource')
        
    Returns:
        list: List of paths to CSV files
    """
    if not os.path.exists(directory):
        return []
    
    if file_type:
        pattern = f"{file_type}-*.csv"
    else:
        pattern = "*.csv"
    
    return glob.glob(os.path.join(directory, pattern))

def extract_date_time_from_filename(filename):
    """
    Extract date and time information from a filename.
    
    Args:
        filename (str): Filename to extract date and time from
        
    Returns:
        tuple: Tuple of (date, time) strings
    """
    # Extract the base filename without path and extension
    base_name = os.path.basename(filename)
    base_name = os.path.splitext(base_name)[0]
    
    # Extract date and time using regex
    match = re.search(r'(\d+-\d+-\d+)(\w+)', base_name)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        return date_str, time_str
    
    return None, None

def ensure_output_dir(date_folder):
    """
    Ensure the output directory exists for the specified date folder.
    
    Args:
        date_folder (str): Date folder name (format: YY-MM-DD)
        
    Returns:
        str: Path to the output directory
    """
    # Create the processed directory if it doesn't exist
    output_dir = os.path.join('assets', 'processed', date_folder)
    os.makedirs(output_dir, exist_ok=True)
    
    return output_dir
