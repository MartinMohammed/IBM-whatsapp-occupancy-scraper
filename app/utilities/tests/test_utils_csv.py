from unittest import (TestCase, mock)
import os 
import csv
from datetime import datetime 
from .. import constants

from .. import utils_csv

@mock.patch("builtins.print")
class TestCSVUtils(TestCase):
    """Tests related to CSV tools."""

    def test_write_to_csv(self, patched_print):
        """
        Test case for write_to_csv function.
        """
        custom_file_path = os.path.join(constants.PATH_TO_ROOT, "data", "test.csv")
        header = ["timestamp", "visitor_count"]
        timestamp = int(datetime.timestamp(datetime.now()))

        # Expect to write a file to the custom file path with one data entry and headers.
        utils_csv.write_to_csv(custom_file_path, header, timestamp, 50)

        with open(custom_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            data = [row for row in csv_reader]

            self.assertTrue(os.path.exists(custom_file_path))
            self.assertEqual(data[0], header)
            self.assertEqual(int(data[1][1]), 50)

        os.remove(custom_file_path)

