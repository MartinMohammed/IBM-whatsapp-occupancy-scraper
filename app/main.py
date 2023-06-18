"""
Author: Martin Mohammed
Application Purpose:

This application serves as a base template for working as a worker and making GET requests to the FitnessFabrik API. The main objective is to collect data as workers and store it in a location where it can be aggregated. 

The ultimate goal is to enable other programs to analyze the fetched data. This application can be cloned multiple times, each dedicated to monitoring the number of visitors in a specific studio.
"""

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



HEADER = ["timestamp", "visitor_count"]
DB_TABLE_NAME = f"visitors_{constants.LOCATION_SHORT_TITLE}"


# --------------- DB CONNECTION ---------------
# wait for the connection to be established
connection = None
cursor = None
# --------------- DB CONNECTION ---------------
 
def main():
    """Fetch from api, and save the result with an timestamp in the visitors.csv file."""
    entries_count = 0 

    # Initial file name
    file_name = utils.construct_visitor_file_name(datetime.now()) 
    is_week_day = utils.check_is_week_day(datetime.now().weekday())
    day = "week_day" if is_week_day else "week_end"

    global connection
    connection = connect_to_db()

    # Initialize starting table if not exists 
    db_schema = "(timestamp TIMESTAMP, visitor_count INT)"
    utils_db.create_table_if_not_exists(connection, table_name=DB_TABLE_NAME, fields=db_schema)


    while True:
        now = datetime.now()
        formatted_timestamp = now.strftime('%Y-%m-%d %H:%M')
        is_in_opening_hours = utils.check_if_in_opening_hours(now.hour, is_week_day)

        # Check if the studio is open based on the current time
        # starts when the gym opens 
        if is_in_opening_hours:
            # Get the JSON response data only for the specific location
            studios_location_data = utils.fetch_data(constants.URL)
            studio_location_data = [studio for studio in studios_location_data if studio["studio_id"] == constants.LOCATION_ID][0]
            assert studio_location_data is not None, f"Studio data for location {constants.LOCATION_ID} \ {constants.LOCATION_SHORT_TITLE} was not found."
            
            entries_count += 1  # Increment entries count

            # Construct a new file after every X entries because the old one was too full
            if entries_count % constants.ENTRIES_UNTIL_FILE_SEGMENTATION == 0:
                file_name = utils.construct_visitor_file_name(datetime.date())
                entries_count = 0  # Reset entries count         
            # =--------------------- SAVE THE DATA ---------------------=
            """
            Before writing to file, check first if a file for the day today already exists. 

            1. Check all files in the current folder
            2. Search current day inside the file name
            """
            visitor_file_name_if_exists = utils.get_today_visitors_file_name_if_it_does_exist(now.year, now.month, now.day)

            # No visitor_file for today was found, allowed to create a new one. 
            if visitor_file_name_if_exists == None: visitor_file_name_if_exists = file_name

            file_path = os.path.join(constants.DATA_DIRECTORY, visitor_file_name_if_exists)

            # data            
            timestamp = int(datetime.timestamp(now))
            current_load = studio_location_data.get("current_load")

            utils_csv.write_to_csv(file_path, HEADER, timestamp, current_load)
            utils_db.save_to_db(connection, table_name=DB_TABLE_NAME, fields="(timestamp, visitor_count)", values=(formatted_timestamp, current_load))
            # =--------------------- SAVE THE DATA ---------------------=

            utils_log.log(message=f"Current load in {constants.LOCATION_SHORT_TITLE}: {current_load}.")

            # Sleep before making the next request
            time.sleep(constants.REQUEST_DENSITY)
        # ends when the gym closes
        else:
            """The studio is closed, sleep until the next day."""   
            opening_time = constants.OPENING_HOURS[day].get("open")
            sleep_seconds = utils.calculate_sleep_time_in_seconds(now, opening_time)

            # integer division 
            sleep_hours = sleep_seconds // 60 // 60
            sleep_minutes = sleep_minutes // 60

            utils_log.log(f"Studio is closed now sleep: {sleep_hours} hours and {sleep_minutes} minutes.")
            time.sleep(sleep_seconds)   

            # ---------------- FINISH SLEEPING ----------------
            utils_log.log(f"Sleeped: {sleep_hours} hours and {sleep_minutes} minutes. Ready to conntinue.")

            # After sleeping create a new file
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
        if cursor:
            cursor.close()
        if connection: 
            connection.close()


