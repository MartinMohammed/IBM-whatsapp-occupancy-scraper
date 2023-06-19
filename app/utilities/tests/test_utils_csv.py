from unittest import TestCase
from unittest.mock import MagicMock, patch
import os
import csv
from datetime import datetime
from .. import constants

from .. import utils_csv


@patch("utilities.utils_log.log")
@patch("builtins.print")
class TestCSVUtils(TestCase):
    """
    Tests related to CSV tools.
    """

    def test_write_to_csv(self, *args):
        """
        Test case for write_to_csv function.
        """
        custom_file_path = os.path.join(constants.LOCATION_DATA_DIR, "test.csv")
        header = ["timestamp", "visitor_count"]
        timestamp = int(datetime.timestamp(datetime.now()))

        # Expect to write a file to the custom file path with one data entry and headers.
        utils_csv.write_to_csv(custom_file_path, header, timestamp, 50)

        with open(custom_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            data = [row for row in csv_reader]

            # Check if the file exists and has the expected data
            self.assertTrue(os.path.exists(custom_file_path), msg="The file should exist.")
            self.assertEqual(data[0], header, msg="The header should match.")
            self.assertEqual(int(data[1][1]), 50, msg="The visitor count should be 50.")

        os.remove(custom_file_path)
