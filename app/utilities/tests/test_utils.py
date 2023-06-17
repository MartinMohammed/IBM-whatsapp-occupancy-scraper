import psycopg2
import psycopg2.extras
import unittest
import os
from unittest import mock
from datetime import datetime

from .. import constants
from .. import utils


@mock.patch("builtins.print")
class TestUtilities(unittest.TestCase):
    """
    Test cases for generic tools.
    """

    def setUp(self):
        """
        Run before every test and do some setup work.
        """
        self.assertion_count = 0  # Initialize assertion count
        self.opening_hours = constants.OPENING_HOURS

        # check if ./data and ./logs folder exists
        data_dir_path = os.path.join(constants.PATH_TO_ROOT, "data")
        if not os.path.exists(data_dir_path):
            os.makedirs(data_dir_path, exist_ok=True)

        logs_dir_path = os.path.join(constants.PATH_TO_ROOT, "logs")
        if not os.path.exists(logs_dir_path):
            os.makedirs(logs_dir_path, exist_ok=True)

    def test_fetch_data(self, _):
        """
        Test case for fetch_data function.
        """
        URL = os.getenv("API_URL")
        with mock.patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": "example data"}
            res_json = utils.fetch_data(URL)
        self.assertEqual(res_json, {"data": "example data"})

    def test_check_is_week_day(self, _):
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

    def test_construct_visitor_file_name(self, _):
        """Test case for the construct_visitor_file_name method."""
        current_time = datetime(year=2023, month=6, day=15, hour=10, minute=30, second=0)
        mocked_timestamp = current_time.strftime("%d-%m-%Y-%H-%M")
        mocked_location_short_title = "FFGR"

        file_name = utils.construct_visitor_file_name(current_time)
        self.assertEqual(file_name, f"visitors-{mocked_location_short_title}-{mocked_timestamp}.csv")

    def test_get_today_visitors_file_name_if_it_does_exist_file_created(self, _):
        """Test if the *visitors* file with the given path already exists when the file was created."""
        now = datetime.now()
        visitor_file_name = utils.construct_visitor_file_name(now)
        visitor_file_path = os.path.join(constants.DATA_DIRECTORY, visitor_file_name)

        # make sure we're not deleting a file that already exists: 
        # When testing, the data folder will not exist. 
        # But when runnning in dev or production it could be that the test would delete the current day file
        if not os.path.exists(visitor_file_path):
            # 1. Create a test file
            with open(visitor_file_path, "w") as _:
                pass


            # 2. Verify that the function returns the file_path because the file already exists in the given folder destination.
            visitor_file_name_test_result = utils.get_today_visitors_file_name_if_it_does_exist(now.month, now.day)
            self.assertEqual(visitor_file_name_test_result, visitor_file_name)

            # Remove the created file
            os.remove(visitor_file_path)


    def test_get_today_visitors_file_name_if_it_does_exist_no_file_created(self, _):
        """Test if the *visitors* file with the given path already exists when no file was created."""
        now = datetime.now()
        visitor_file_name = utils.construct_visitor_file_name(now)
        visitor_file_path = os.path.join(constants.DATA_DIRECTORY, visitor_file_name)
        if not os.path.exists(visitor_file_path):
            visitor_file = utils.get_today_visitors_file_name_if_it_does_exist(now.month, now.day)
            self.assertEqual(visitor_file, None)

    def test_check_if_in_opening_hours_week_day(self, _):
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

    def test_check_if_in_opening_hours_week_end(self, _):
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

    def test_calculate_sleep_time_in_seconds(self, _):
        """
        Test case for the calculate_sleep_time_in_seconds function.
        Checks if it returns the correct amount of seconds until the opening time tomorrow.
        """

        current_time = datetime(year=2023, month=6, day=15, hour=23, minute=34, second=35)
        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 8)

        self.assertEqual(amount_of_seconds, 30325)

        current_time = datetime(year=2023, month=6, day=15, hour=0, minute=40, second=55)
        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 11)

        self.assertEqual(amount_of_seconds, 37145)
