"""
Author: Martin Mohammed
Application Purpose:

This application serves as a base template for working as a worker and making GET requests to the FitnessFabrik API.
The main objective is to collect data as workers and store it in a location where it can be aggregated.

The ultimate goal is to enable other programs to analyze the fetched data.
This application can be cloned multiple times, each dedicated to monitoring the number of visitors in a specific studio.
"""

import os
import time
from datetime import datetime, timedelta
import sys

from utilities import (
    constants,
    utils,
    utils_csv,
    utils_db,
    utils_log
)

from utilities.management.db_connect import connect_to_db

HEADER = ["timestamp", "visitor_count"]
DB_TABLE_NAME = f"visitors_{constants.LOCATION_SHORT_TITLE}"

# --------------- DB CONNECTION ---------------

try:
    # Check if DB_HOSTNAME is provided
    DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
    assert DB_HOSTNAME, "DB_HOSTNAME environment variable is not set."

    # Check if DB_NAME is provided
    DB_NAME = os.environ.get("DB_NAME").replace("-", "_")
    assert DB_NAME, "DB_NAME environment variable is not set."

    # Check if DB_USERNAME is provided
    DB_USERNAME = os.environ.get("DB_USERNAME")
    assert DB_USERNAME, "DB_USERNAME environment variable is not set."

    # Check if DB_PASSWORD is provided
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    assert DB_PASSWORD, "DB_PASSWORD environment variable is not set."

    # Check if DB_PORT is provided
    DB_PORT = os.environ.get("DB_PORT")
    assert DB_PORT, "DB_PORT environment variable is not set."

except AssertionError as e:
    error_file_path = os.path.join(constants.LOG_DIRECTORY, "logs.error")
    utils_log.log(f"Location Short Title: {constants.LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)

# Global variables.
db_connection = None
# --------------- DB CONNECTION ---------------


def main():
    """
    Fetch data from the API and save the result with a timestamp in the visitors.csv file.
    """
    entries_count = 0
    now = datetime.now()

    # Initial file name
    file_name = utils.construct_visitor_file_name(now)
    is_week_day = utils.check_is_week_day(now.weekday())
    day = "week_day" if is_week_day else "week_end"

    global connection
    db_connection = connect_to_db(
        db_host=DB_HOSTNAME,
        db_name=DB_NAME,
        db_user=DB_USERNAME,
        db_password=DB_PASSWORD,
        db_port=DB_PORT,
        recursion_depth=0
    )

    # Initialize starting table if it does not exist
    db_schema = "(timestamp TIMESTAMP, visitor_count INT)"
    utils_db.create_table_if_not_exists(db_connection, table_name=DB_TABLE_NAME, fields=db_schema)

    position_of_studio = None

    while True:
        now = datetime.now()
        formatted_timestamp = now.strftime('%Y-%m-%d %H:%M')
        is_in_opening_hours = utils.check_if_in_opening_hours(now.hour, is_week_day)

        # Check if the studio is open based on the current time (starts when the gym opens)
        if is_in_opening_hours:
            # Get the JSON response data only for the specific location
            studios_location_data = utils.fetch_data(constants.URL)

            if position_of_studio is None:
                for i, studio in enumerate(studios_location_data):
                    if studio["studio_id"] == constants.STUDIO_ID:
                        position_of_studio = i

            studio_location_data = studios_location_data[position_of_studio]
            assert studio_location_data is not None, f"Studio data for location {constants.LOCATION_ID} / {constants.LOCATION_SHORT_TITLE} was not found."

            entries_count += 1  # Increment entries count

            # Construct a new file after every X entries because the old one was too full
            if entries_count % constants.ENTRIES_UNTIL_FILE_SEGMENTATION == 0:
                file_name = utils.construct_visitor_file_name(datetime.date())
                entries_count = 0  # Reset entries count

            # Save the data to file
            """
            Before writing to file, check if a file for the current day already exists.

            1. Check all files in the current folder
            2. Search for the current day in the file name
            """
            visitor_file_name_if_exists = utils.get_today_visitors_file_name_if_it_does_exist(now.year, now.month, now.day)

            # No visitor_file for today was found, create a new one.
            if visitor_file_name_if_exists is None:
                visitor_file_name_if_exists = file_name

            file_path = os.path.join(constants.DATA_DIRECTORY, visitor_file_name_if_exists)

            timestamp = int(datetime.timestamp(now))
            current_load = studio_location_data.get("current_load")

            utils_csv.write_to_csv(file_path, HEADER, timestamp, current_load)

            # Save the data to the database
            """
            Before writing to the database, make sure the database table exists.
            """
            utils_db.save_to_db(db_connection, table_name=DB_TABLE_NAME, fields="(timestamp, visitor_count)", values=(formatted_timestamp, current_load))

            utils_log.log(message=f"Current load in {constants.LOCATION_SHORT_TITLE}: {current_load}.")

            # Sleep before making the next request
            time.sleep(constants.REQUEST_DENSITY)
        else:
            """
            The studio is closed, sleep until the next day.
            """
            opening_time = constants.OPENING_HOURS[day].get("open")
            sleep_seconds = utils.calculate_sleep_time_in_seconds(now, opening_time)

            # Calculate sleep hours and minutes
            sleep_hours = sleep_seconds // 60 // 60
            sleep_minutes = (int(sleep_seconds / 60)) - sleep_hours * 60

            utils_log.log(f"Studio is closed, now sleep: {sleep_hours} hours and {sleep_minutes} minutes.")
            time.sleep(sleep_seconds)

            # After sleeping, create a new file
            time_after_sleeping = now + timedelta(hours=sleep_hours, minutes=sleep_minutes)

            file_name = utils.construct_visitor_file_name(time_after_sleeping)
            is_week_day = utils.check_is_week_day(time_after_sleeping.weekday())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Handle the exception, e.g., print an error message
        print("An exception occurred:", str(e))
    finally:
        # Close the database connection in the finally block
        if db_connection:
            db_connection.close()
