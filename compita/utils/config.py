"""
Configuration management for the Cyber8 report generator.
"""
import os
import json
from pathlib import Path

class Config:
    """Configuration manager for the Cyber8 report generator."""
    
    def __init__(self):
        """Initialize the configuration."""
        self.base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.assets_dir = self.base_dir / 'assets'
        self.reports_dir = self.base_dir / 'reports'
        self.templates_dir = self.base_dir / 'templates'
        self.static_dir = self.base_dir / 'static'
    
    def get_processed_data_path(self, date, file_type):
        """Get the path to processed data files."""
        if file_type == 'gradebook':
            return self.assets_dir / 'processed' / date / f'classgradebook-{date.replace("-", "-")}-5pm.json'
        elif file_type == 'study':
            return self.assets_dir / 'processed' / date / f'classstudyhistory-{date.replace("-", "-")}-4pm.json'
        elif file_type == 'resource':
            return self.assets_dir / 'processed' / date / f'timeperresource-{date.replace("-", "-")}-5pm.json'
        else:
            raise ValueError(f"Unknown file type: {file_type}")
    
    def get_reports_path(self, date, report_type=None):
        """Get the path to report output directories."""
        if report_type == 'progress':
            return self.reports_dir / date / 'progress_reports'
        elif report_type == 'assessment':
            return self.reports_dir / date / 'assessment_reports'
        elif report_type == 'grades':
            return self.reports_dir / date / 'grades_reports'
        elif report_type == 'executive':
            return self.reports_dir / date / 'executive_reports'
        elif report_type == 'metrics':
            return self.reports_dir / date / 'metrics'
        elif report_type == 'student_reports':
            return self.reports_dir / date / 'progress_reports' / 'student_reports'
        elif report_type == 'class_summaries':
            return self.reports_dir / date / 'progress_reports' / 'class_summaries'
        else:
            return self.reports_dir / date
    
    def ensure_directories(self, date):
        """Ensure all necessary directories exist."""
        directories = [
            self.get_reports_path(date),
            self.get_reports_path(date, 'progress'),
            self.get_reports_path(date, 'assessment'),
            self.get_reports_path(date, 'grades'),
            self.get_reports_path(date, 'executive'),
            self.get_reports_path(date, 'metrics'),
            self.get_reports_path(date, 'student_reports'),
            self.get_reports_path(date, 'class_summaries'),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        return True

# Create a singleton instance
config = Config()
