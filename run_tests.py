#!/usr/bin/env python3
"""
Test runner for the CompITA report generator.
"""
import unittest
import sys
from pathlib import Path

def run_tests():
    """Run all tests in the tests directory."""
    # Discover and run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
