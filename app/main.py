"""
Author: Martin Mohammed
Application Purpose:

This application serves as a base template for working as a worker and making GET requests to the FitnessFabrik API. The main objective is to collect data as workers and store it in a location where it can be aggregated. 

The ultimate goal is to enable other programs to analyze the fetched data. This application can be cloned multiple times, each dedicated to monitoring the number of visitors in a specific studio.
"""

import sys
import os
import time
from datetime import datetime, timedelta

from utilities import (
    constants,
    utils,
    utils_csv,
    utils_db, 
    utils_log
    )

from utilities.management.db_connect import connect_to_db


# ----------------------- SETTINGS -----------------------
REQUEST_DENSITY = 60 * int(os.getenv("REQUEST_DENSITY") or 5)  # Specifies the frequency of API requests in seconds.
ENTRIES_UNTIL_FILE_SEGMENTATION = int(os.getenv("ENTRIES_UNTIL_FILE_SEGMENTATION") or 1000)  # How many entries in the CSV file until a new one is created.

# Required Environment variables:
try:
    assert isinstance(REQUEST_DENSITY, int), "REQUEST_DENSITY must be a valid integer."
    assert isinstance(ENTRIES_UNTIL_FILE_SEGMENTATION, int), "ENTRIES_UNTIL_FILE_SEGMENTATION must be a valid integer."

    LOCATION_ID = os.getenv("LOCATION_ID")  # The ID of the gym location.
    assert LOCATION_ID is not None, "LOCATION_ID was not provided."

    LOCATION_SHORT_TITLE = os.getenv("LOCATION_SHORT_TITLE")  # Indicates the location to be tracked based on the gym-mapping.json file.
    assert LOCATION_SHORT_TITLE is not None, "LOCATION_SHORT_TITLE was not provided."

    URL = os.getenv("API_URL")
    assert URL is not None, "API_URL was not provided."

    LOCATION_ID = int(LOCATION_ID)
except AssertionError as e:
    error_file_path = os.path.join(constants.LOG_DIRECTORY, "logs.error")
    utils_log.log(f"Location Short Title: {LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)

# ----------------------- SETTINGS -----------------------
HEADER = ["timestamp", "visitor_count"]
DB_TABLE_NAME = f"visitors_{LOCATION_SHORT_TITLE}"


# --------------- DB CONNECTION ---------------
# wait for the connection to be established
connection = None
cursor = None
# --------------- DB CONNECTION ---------------
 
def main():
    """Fetch from api, and save the result with an timestamp in the visitors.csv file."""
    entries_count = 0 

    # Initial file name
    file_name = utils.construct_file_name(datetime.now(), LOCATION_SHORT_TITLE) 
    is_week_day = utils.check_is_week_day(datetime.now().weekday())
    day = "week_day" if is_week_day else "week_end"

    global connection
    connection = connect_to_db()

    # Initialize starting table if not exists 
    db_schema = "(timestamp TIMESTAMP, visitor_count INT)"
    utils_db.create_table_if_not_exists(connection, table_name=DB_TABLE_NAME, fields=db_schema)


    while True:
        now = datetime.now()
        is_in_opening_hours = utils.check_if_in_opening_hours(now.hour, is_week_day)

        # Check if the studio is open based on the current time
        # starts when the gym opens 
        if is_in_opening_hours:
            # Get the JSON response data only for the specific location
            studios_location_data = utils.fetch_data(URL)
            studio_location_data = [studio for studio in studios_location_data if studio["studio_id"] == LOCATION_ID][0]
            assert studio_location_data is not None, f"Studio data for location {LOCATION_ID} \ {LOCATION_SHORT_TITLE} was not found."
            
            entries_count += 1  # Increment entries count

            # Construct a new file after every X entries because the old one was too ful 
            if entries_count % ENTRIES_UNTIL_FILE_SEGMENTATION == 0:
                utils.construct_file_name(datetime.date(), LOCATION_SHORT_TITLE)
                entries_count = 0  # Reset entries count

            file_path = os.path.join(constants.DATA_DIRECTORY, file_name)
            timestamp = int(datetime.timestamp(now))
            
            current_load = studio_location_data.get("current_load")

            # =--------------------- SAVE THE DATA ---------------------=
            utils_csv.write_to_csv(file_path, HEADER, timestamp, current_load)
            utils_db.save_to_db(connection, table_name=DB_TABLE_NAME, values=(now.strftime('%Y-%m-%d %H:%M'), current_load))
            # =--------------------- SAVE THE DATA ---------------------=

            utils_log.log(message=f"Current load in {LOCATION_SHORT_TITLE}: {current_load}.")

            # Sleep before making the next request
            time.sleep(REQUEST_DENSITY)
        # ends when the gym closes
        else:
            """The studio is closed, sleep until the next day."""   
            opening_time = constants.OPENING_HOURS[day].get("open")
            sleep_seconds = utils.calculate_sleep_time_in_seconds(now, opening_time, tomorrow=now.hour >= opening_time)

            # integer division 
            sleep_hours = sleep_seconds // 60 // 60

            utils_log.log(f"Now sleep: {sleep_hours} hours.")
            time.sleep(sleep_seconds)   

            # ---------------- FINISH SLEEPING ----------------
            utils_log.log(f"Sleeped: {sleep_hours} hours.")

            # After sleeping create a new file
            time_after_sleeping = now + timedelta(hours=sleep_hours)

            file_name = utils.construct_file_name(time_after_sleeping, LOCATION_SHORT_TITLE)
            is_week_day = utils.check_is_week_day(time_after_sleeping.weekday())

            
if __name__ == "__main__":
    try: 
        main()
    except Exception as e: 
        # Handle the exception, e.g., print an error message
        print("An exception occurred:", str(e))
    finally: 
       # Close the database connection in the finally block
        if cursor:
            cursor.close()
        if connection: 
            connection.close()


