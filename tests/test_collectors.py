"""
Tests for the collectors module.
"""
import unittest
import os
import tempfile
import json
from pathlib import Path

# Add parent directory to path to allow importing during testing
import sys
sys.path.append(str(Path(__file__).parent.parent))

from compita.utils.helpers import format_time_seconds, normalize_student_name

class TestCollectorUtils(unittest.TestCase):
    """Test cases for collector utility functions."""
    
    def test_format_time_seconds(self):
        """Test formatting seconds to time string."""
        # Test with zero seconds
        self.assertEqual(format_time_seconds(0), "0s")
        
        # Test with only seconds
        self.assertEqual(format_time_seconds(45), "45s")
        
        # Test with minutes and seconds
        self.assertEqual(format_time_seconds(125), "2m 5s")
        
        # Test with hours, minutes, and seconds
        self.assertEqual(format_time_seconds(3665), "1h 1m 5s")
        
        # Test with only hours and seconds
        self.assertEqual(format_time_seconds(3600), "1h")
        
        # Test with None
        self.assertEqual(format_time_seconds(None), "0s")
    
    def test_normalize_student_name(self):
        """Test normalizing student names."""
        # Test with normal name
        self.assertEqual(normalize_student_name("John Doe"), "John Doe")
        
        # Test with leading and trailing whitespace
        self.assertEqual(normalize_student_name("  John Doe  "), "John Doe")
        
        # Test with None
        self.assertIsNone(normalize_student_name(None))
        
        # Test with empty string
        self.assertEqual(normalize_student_name(""), "")

if __name__ == '__main__':
    unittest.main()
