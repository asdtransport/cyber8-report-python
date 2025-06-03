"""
Tests for the converters module.
"""
import unittest
import os
import tempfile
from pathlib import Path

# Add parent directory to path to allow importing during testing
import sys
sys.path.append(str(Path(__file__).parent.parent))

class TestMarkdownToPDF(unittest.TestCase):
    """Test cases for markdown to PDF conversion."""
    
    def test_markdown_to_pdf_args(self):
        """Test argument parsing for markdown to PDF conversion."""
        # Import the module
        import markdown_to_pdf
        original_main = markdown_to_pdf.main
        
        try:
            # Replace main with a function that captures sys.argv
            captured_args = []
            def mock_main():
                captured_args.append(list(sys.argv))
                return True
            
            markdown_to_pdf.main = mock_main
            
            # Import the adapter module
            from compita.converters.markdown_to_pdf import convert_markdown_to_pdf
            
            # Test with required arguments
            input_dir = "reports/25-05-05/progress_reports/student_reports"
            output_dir = "reports/25-05-05/executive_reports"
            convert_markdown_to_pdf(input_dir, output_dir)
            
            self.assertEqual(captured_args[0][0], 'markdown_to_pdf.py')
            self.assertEqual(captured_args[0][1], '--input-dir')
            self.assertEqual(captured_args[0][2], input_dir)
            self.assertEqual(captured_args[0][3], '--output-dir')
            self.assertEqual(captured_args[0][4], output_dir)
            
        finally:
            # Restore original main function
            markdown_to_pdf.main = original_main

if __name__ == '__main__':
    unittest.main()
