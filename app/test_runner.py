"""
The test runner will discover and execute all the tests in the specified modules or packages and display the test results in the console.
"""
import unittest
import sys

# Import the test modules or packages
from utilities.tests import test_utils
from utilities.management.tests import test_db_connection

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Load tests from modules or packages
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_utils))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_db_connection))

    # Create a test runner and run the suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)  # Exit with non-zero code if there were test failures/errors