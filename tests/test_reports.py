"""
Tests for the reports module.
"""
import unittest
import os
import tempfile
import json
from pathlib import Path

# Add parent directory to path to allow importing during testing
import sys
sys.path.append(str(Path(__file__).parent.parent))

class TestReportGeneration(unittest.TestCase):
    """Test cases for report generation functionality."""
    
    def test_flexible_module_report_args(self):
        """Test argument parsing for flexible module report."""
        from compita.reports.flexible_module import generate_flexible_module_report
        
        # Mock the main function to capture arguments
        import flexible_module_report
        original_main = flexible_module_report.main
        
        try:
            # Replace main with a function that captures sys.argv
            captured_args = []
            def mock_main():
                captured_args.append(list(sys.argv))
                return True
            
            flexible_module_report.main = mock_main
            
            # Test with minimal arguments
            generate_flexible_module_report('25-05-05')
            self.assertEqual(captured_args[0][0], 'flexible_module_report.py')
            self.assertEqual(captured_args[0][1], '--date')
            self.assertEqual(captured_args[0][2], '25-05-05')
            
            # Test with all arguments
            captured_args.clear()
            generate_flexible_module_report(
                '25-05-05',
                all_modules=['1', '2', '3'],
                subset_modules=['2', '3'],
                exclude_modules=['4'],
                output_prefix='test_prefix',
                count_partial=True
            )
            
            self.assertIn('--all-modules', captured_args[0])
            self.assertIn('1', captured_args[0])
            self.assertIn('--subset-modules', captured_args[0])
            self.assertIn('--exclude-modules', captured_args[0])
            self.assertIn('--output-prefix', captured_args[0])
            self.assertIn('test_prefix', captured_args[0])
            self.assertIn('--count-partial', captured_args[0])
            
        finally:
            # Restore original main function
            flexible_module_report.main = original_main

if __name__ == '__main__':
    unittest.main()
