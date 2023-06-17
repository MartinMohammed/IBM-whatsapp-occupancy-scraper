import os
from unittest import (TestCase, mock)

from .. import constants
from .. import utils_log

@mock.patch("builtins.print")
class TestLogUtils(TestCase):

    # --------------------- FOR LOG ---------------------S
    def test_log_file_path_provided(self, patched_print):
        """Test case for the log function."""
        custom_file_path = os.path.join(constants.PATH_TO_ROOT, "logs", "error.log")
        error_message = "Error."
        utils_log.log(error_message, custom_file_path)

        # Check if log writes to file
        self.assertTrue(os.path.exists(custom_file_path))

        # Check content of logged file
        with open(custom_file_path, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn(error_message, log_contents)

        # Remove the redundant file:
        os.remove(custom_file_path)

    def test_log_file_path_not_provided(self, patched_print):
        """Test case for log function to check if file is created when no file path is provided."""
        log_message = "Error."
        utils_log.log(log_message)
        self.assertFalse(os.path.exists(os.path.join(constants.PATH_TO_ROOT, "logs", "error.log")))

    # --------------------- FOR LOG --------------------- #