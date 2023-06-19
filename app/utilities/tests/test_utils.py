import unittest
import os
import shutil
from unittest.mock import patch
from datetime import datetime
import time

from .. import constants
from .. import utils


@patch("utilities.utils_log.log")
@patch("builtins.print")
class TestUtilities(unittest.TestCase):
    """
    Test cases for generic tools.
    """

    def setUp(self):
        """
        Set up before every test by performing some initial setup work.
        """
        self.assertion_count = 0  # Initialize assertion count
        self.opening_hours = constants.OPENING_HOURS

        # Check if the './data' and './logs' folders inside the studio short name dir. exist
        if not os.path.exists(constants.LOCATION_DATA_DIR):
            os.makedirs(constants.LOCATION_DATA_DIR, exist_ok=True)

        if not os.path.exists(constants.LOCATION_LOG_DIR):
            os.makedirs(constants.LOCATION_LOG_DIR, exist_ok=True)

    def tearDown(self):
     # Clean up the created directories from setUp.
        """
        To address this issue, you can use shutil.rmtree() instead of os.removedirs() to recursively remove the directories and their contents,
        regardless of whether they are empty or not. Here's an updated version of the tearDown() method that uses shutil.rmtree():
         """
        # if os.path.exists(constants.LOCATION_DATA_DIR):
        #     shutil.rmtree(constants.LOCATION_DATA_DIR)

        # if os.path.exists(constants.LOCATION_LOG_DIR):
        #     shutil.rmtree(constants.LOCATION_LOG_DIR)

    def test_fetch_data(self, *args):
        """
        Test case for the fetch_data function.
        """
        URL = os.getenv("API_URL")
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": "example data"}
            res_json = utils.fetch_data(URL)
        self.assertEqual(res_json, {"data": "example data"})

    def test_check_is_week_day(self, *args):
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

    def test_construct_visitor_file_name(self, *args):
        """Test case for the construct_visitor_file_name method."""
        current_time = datetime(year=2023, month=6, day=15, hour=10, minute=30, second=0)
        mocked_timestamp = current_time.strftime("%d-%m-%Y-%H-%M")

        file_name = utils.construct_visitor_file_name(current_time)
        self.assertEqual(file_name, f"visitors-{constants.LOCATION_SHORT_TITLE}-{mocked_timestamp}.csv")

    def test_get_today_visitors_file_name_if_it_does_exist_file_created(self, *args):
        """Test if the *visitors* file with the given path already exists when the file was created."""
        patched_log = args[1]
        now = datetime.now()
        now = now.replace(year=1980)  # Demo year.

        visitor_file_name = utils.construct_visitor_file_name(now)
        visitor_file_path = os.path.join(constants.LOCATION_DATA_DIR, visitor_file_name)

        # 1. Create a test file
        with open(visitor_file_path, "w") as _:
            pass

        # 2. Verify that the function returns the file_path because the file already exists in the given folder destination.
        visitor_file_name_test_result = utils.get_today_visitors_file_name_if_it_does_exist(
            now.year,
            now.month,
            now.day
            )
        
        self.assertEqual(visitor_file_name_test_result, visitor_file_name)

        log_message = f"Found an existing file, continue writing there: {visitor_file_name}."
        patched_log.assert_called_with(log_message)

        # Remove the created file
        os.remove(visitor_file_path)

    def test_get_today_visitors_file_name_if_it_does_exist_no_file_created(self, *args):
        """Test if the *visitors* file with the given path already exists when no file was created."""
        patched_log = args[1]
        now = datetime.now()
        now = now.replace(year=1980)  # Demo year.

        day = now.day
        month = now.month
        year = now.year

        visitor_file = utils.get_today_visitors_file_name_if_it_does_exist(year, month, day)
        self.assertEqual(visitor_file, None)

        if now.day < 10:
            day = f"0{now.day}"
        if now.month < 10:
            month = f"0{now.month}"
        log_message = f"Did not find an existing file for day: {day}, month: {month}, {year}, create a new file."
        patched_log.assert_called_with(log_message)

    def test_check_if_in_opening_hours_week_day(self, *args):
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

    def test_check_if_in_opening_hours_week_end(self, *args):
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

    def test_calculate_sleep_time_in_seconds_for_tomorrow(self, *args):
        """
        Test case for the calculate_sleep_time_in_seconds function.
        Checks if it returns the correct amount of seconds until the opening time tomorrow.
        """
        current_time = datetime(year=2023, month=6, day=15, hour=23, minute=34, second=35)
        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 8)

        self.assertEqual(amount_of_seconds, 30325)

    def test_calculate_sleep_time_in_seconds_for_today(self, *args): 
       # today 
        current_time = datetime(year=2023, month=6, day=16, hour=3, minute=40, second=55)
        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 8)

        self.assertEqual(amount_of_seconds, 15545)

        # 5:29 AM and 20 seconds 
        current_time = datetime(year=2023, month=6, day=16, hour=5, minute=29, second=20)

        amount_of_seconds = utils.calculate_sleep_time_in_seconds(current_time, 8)
        self.assertEqual(amount_of_seconds, 9040)

