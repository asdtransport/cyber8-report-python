"""
Tests for the parsers module.
"""
import unittest
import os
import tempfile
import json
from pathlib import Path

# Add parent directory to path to allow importing during testing
import sys
sys.path.append(str(Path(__file__).parent.parent))

from compita.parsers.utils import find_latest_date_folder, find_csv_files, extract_date_time_from_filename, ensure_output_dir

class TestParserUtils(unittest.TestCase):
    """Test cases for parser utility functions."""
    
    def test_extract_date_time_from_filename(self):
        """Test extracting date and time from filenames."""
        # Test with valid filename
        date_str, time_str = extract_date_time_from_filename('classgradebook-5-05-5pm.csv')
        self.assertEqual(date_str, '5-05-5')
        self.assertEqual(time_str, 'pm')
        
        # Test with another valid filename
        date_str, time_str = extract_date_time_from_filename('timeperresource-05-05-5pm.csv')
        self.assertEqual(date_str, '05-05-5')
        self.assertEqual(time_str, 'pm')
        
        # Test with invalid filename
        date_str, time_str = extract_date_time_from_filename('invalid_filename.csv')
        self.assertIsNone(date_str)
        self.assertIsNone(time_str)
    
    def test_ensure_output_dir(self):
        """Test ensuring output directory exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change working directory to temp directory
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Create assets directory
                os.makedirs(os.path.join('assets', 'processed'), exist_ok=True)
                
                # Test ensuring output directory
                output_dir = ensure_output_dir('25-05-05')
                self.assertTrue(os.path.exists(output_dir))
                self.assertEqual(output_dir, os.path.join('assets', 'processed', '25-05-05'))
            finally:
                # Change back to original directory
                os.chdir(original_dir)

if __name__ == '__main__':
    unittest.main()
