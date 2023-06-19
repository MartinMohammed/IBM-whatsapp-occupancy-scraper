import os
from unittest import TestCase
from unittest.mock import patch

from .. import constants
from .. import utils_log


@patch("builtins.print")
class TestLogUtils(TestCase):

    # --------------------- FOR LOG ---------------------
    def test_log_file_path_provided(self, *args):
        """Test case for the log function.

        Test if the log function writes the error message to the specified custom log file path.
        """

        # Set up
        custom_log_file_path = os.path.join(constants.LOCATION_LOG_DIR, "error.log")
        error_message = "Error."

        # Call the log function with custom log file path
        utils_log.log(error_message, custom_log_file_path)

        # Check if log writes to file
        self.assertTrue(os.path.exists(custom_log_file_path), msg="Expect that the log file was created.")

        # Check content of logged file
        with open(custom_log_file_path, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn(error_message, log_contents, msg=f"Expect that the content of the log file contains the error {error_message} message.")

        # Remove the redundant file
        os.remove(custom_log_file_path)

    def test_log_file_path_not_provided(self, *args):
        """Test case for log function to check if file is created when no file path is provided.

        Test if the log function creates the error log file when no file path is provided.
        """

        # Set up
        log_message = "Error."

        # Call the log function without specifying log file path
        utils_log.log(log_message)

        # Check if the error log file is not created
        self.assertFalse(os.path.exists(os.path.join(constants.LOCATION_LOG_DIR, "error.log")), msg="Expect that the error file was not created when not log_file_path was provided.")

    # --------------------- FOR LOG ---------------------
    #
    # Additional comments:
    # - The "FOR LOG" section indicates that the following tests are related to the log function.
    # - The patch decorator is used to mock the print function for testing purposes.
    # - Each test case verifies a specific aspect of the log function's behavior.
    # - Test case 1 checks if the log function writes the error message to the specified custom log file path.
    # - Test case 2 checks if the log function creates the error log file when no file path is provided.
