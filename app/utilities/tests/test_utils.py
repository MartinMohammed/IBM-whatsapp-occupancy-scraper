import psycopg2
import psycopg2.extras
import unittest
import os
from unittest import mock
import csv
from datetime import datetime

from .. import constants
from .. import utils

@mock.patch("builtins.print")
class TestUtilities(unittest.TestCase):
    """
    Test cases for string methods.
    """

    def setUp(self):
        """
        Run before every test and do some setup work.
        """
        self.assertion_count = 0  # Initialize assertion count
        self.opening_hours = constants.OPENING_HOURS
        self.app_path = os.getcwd()

        # check if ./data and ./logs folder exists 
        data_dir_path = os.path.join(self.app_path, "data")
        if not os.path.exists(data_dir_path):
            os.makedirs(data_dir_path, exist_ok=True)

        logs_dir_path = os.path.join(self.app_path, "logs")
        if not os.path.exists(logs_dir_path):
            os.makedirs(logs_dir_path, exist_ok=True)



            

    def test_fetch_data(self, patched_print):
        """
        Test case for fetch_data function.
        """
        URL = os.getenv("API_URL")
        with mock.patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": "example data"}
            res_json = utils.fetch_data(URL)
        self.assertEqual(res_json, {"data": "example data"})

    def test_write_to_csv(self, patched_print):
        """
        Test case for write_to_csv function.
        """
        custom_file_path = os.path.join(self.app_path, "data", "test.csv")
        header = ["timestamp", "visitor_count"]
        timestamp = int(datetime.timestamp(datetime.now()))

        # Expect to write a file to the custom file path with one data entry and headers.
        utils.write_to_csv(custom_file_path, header, timestamp, 50)

        with open(custom_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            data = [row for row in csv_reader]

            self.assertTrue(os.path.exists(custom_file_path))
            self.assertEqual(data[0], header)
            self.assertEqual(int(data[1][1]), 50)

        # Remove the redundant file:
        if os.path.exists(custom_file_path):
            os.remove(custom_file_path)

    # --------------------- FOR LOG ---------------------S
    def test_log_file_path_provided(self, patched_print):
        """Test case for the log function."""
        custom_file_path = os.path.join(self.app_path, "logs", "error.log")
        error_message = "Error."
        utils.log(error_message, custom_file_path)

        # Check if log writes to file
        self.assertTrue(os.path.exists(custom_file_path))

        # Check content of logged file
        with open(custom_file_path, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn(error_message, log_contents)

        # Remove the redundant file:
        if os.path.exists(custom_file_path):
            os.remove(custom_file_path)

    def test_log_file_path_not_provided(self, patched_print):
        """Test case for log function to check if file is created when no file path is provided."""
        log_message = "Error."
        utils.log(log_message)
        self.assertFalse(os.path.exists(os.path.join(self.app_path, "logs", "error.log")))

    # --------------------- FOR LOG ---------------------S


    def test_check_is_week_day(self, patched_print):
        """
        Test case to check if the current day is a week day (Monday to Friday).
        """
        # 0 = Monday, 4 = Friday
        days = [0, 4, 5, 6]
        results = [True, True, False, False]
        for (day, result) in zip(days, results):
            self.assertEqual(utils.check_is_week_day(day), result)
            self.assertion_count += 1
        self.assertEqual(self.assertion_count, len(days))

    def test_construct_file_name(self, patched_print):
        """Test case for the construct_file_name method."""
        current_time = datetime(year=2023, month=6, day=15, hour=10, minute=30, second=0)
        mocked_timestamp = current_time.strftime("%d-%m-%Y-%H-%M")
        mocked_location_short_title = "FFGR"

        file_name = utils.construct_file_name(current_time, mocked_location_short_title)
        self.assertEqual(file_name, f"visitors-{mocked_location_short_title}-{mocked_timestamp}.csv")

    def test_check_if_in_opening_hours_week_day(self, patched_print):
        """
        Test case to check if the current time is within the opening hours of the Griesheim gym on weekdays.
        """
        open_hour = self.opening_hours["week_day"].get("open")
        close_hour = self.opening_hours["week_day"].get("close")
        hours = [open_hour - 1, open_hour, close_hour, close_hour + 1]
        results = [False, True, False, False]
        is_week_day = True

        for (hour, result) in zip(hours, results):
            res = utils.check_if_in_opening_hours(hour, is_week_day=is_week_day)
            self.assertEqual(res, result)
            self.assertion_count += 1

        self.assertEqual(self.assertion_count, len(hours))

    def test_check_if_in_opening_hours_week_end(self, patched_print):
        """Test case for checking if the current hour is within the opening hours of the Griesheim gym on weekends."""
        open_hour = self.opening_hours["week_end"].get("open")
        close_hour = self.opening_hours["week_end"].get("close")
        hours = [open_hour - 1, open_hour, close_hour, close_hour + 1]
        results = [False, True, False, False]
        is_week_day = False

        for (hour, result) in zip(hours, results):
            res = utils.check_if_in_opening_hours(hour, is_week_day=is_week_day)
            self.assertEqual(res, result)
            self.assertion_count += 1

        self.assertEqual(self.assertion_count, len(hours))

    def test_calculate_sleep_time_in_seconds(self, patched_print):
        """
        Test case for the calculate_sleep_time_in_seconds function.
        Checks if it returns the correct amount of seconds until the opening time tomorrow.
        """

        current_time = datetime(year=2023, month=6, day=15, hour=23, minute=34, second=35)
        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 8)

        self.assertEqual(amount_of_seconds, 30325)

        current_time = datetime(year=2023, month=6, day=15, hour=0, minute=40, second=55)
        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 11, tomorrow=False)

        self.assertEqual(amount_of_seconds, 37145)

    # --------------------- FOR DATABASE --------------------- #
    def test_create_table_if_not_exists(self, patched_print):
        """
        Test if the create_table_if_not_exists method constructs a correct query to execute.

        Args:
            patched_print: Patched print object.

        Raises:
            AssertionError: If the execute method was not called with the correct arguments or
                            if the connection commit method was not called.

        """
        # Create mock cursor and connection
        mock_cursor = mock.MagicMock()
        mock_connection = mock.MagicMock()

        # Mock the connection.cursor method to return a mocked context manager.
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        table_name = "visitors"
        fields = "(timestamp TIMESTAMP, visitor_count INT)"
        utils.create_table_if_not_exists(connection=mock_connection, table_name=table_name, fields=fields)

        # Check if the execute method was called with the correct arguments
        expected_query = f"CREATE TABLE IF NOT EXISTS {table_name}{fields}"
        mock_cursor.execute.assert_called_once_with(expected_query)

        # Check if connection commit method was called
        mock_connection.commit.assert_called_once()


    def test_save_to_db(self, patched_print):
        """
        Check if the save_to_db method creates the correct query for the cursor to execute.

        Args:
            patched_print: Patched print object.

        Raises:
            AssertionError: If the execute method was not called with the correct query and values or
                            if the connection commit method was not called.

        """
        mock_cursor = mock.MagicMock()
        mock_connection = mock.MagicMock()

        # connection.cursor() returns us a context manager.
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        table_name = "visitors"
        timestamp = 1000
        visitor_count = 59

        utils.save_to_db(connection=mock_connection, table_name=table_name, values=(timestamp, visitor_count))
        expected_query = f"INSERT INTO {table_name} (timestamp, visitor_count) VALUES(%s, %s)"

        # Check if cursor.execute has correct constructed query in order to insert
        mock_cursor.execute.assert_called_once_with(expected_query, (timestamp, visitor_count))

        # Check if connection.commit() was called once.
        mock_connection.commit.assert_called_once()





# Run this program as a module only
if __name__ == '__main__':
    unittest.main()
