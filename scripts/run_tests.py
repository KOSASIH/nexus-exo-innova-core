# scripts/run_tests.py

import unittest
import os

def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')  # Assuming tests are in the 'tests' directory
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

if __name__ == "__main__":
    run_tests()
