# db_connect.py
"""Module for doing some setup like connecting to an DB."""
import os 
import sys
import time
import psycopg2
from .. import utils
from .. import constants

# ----------------------- DATABASE CONNECTION -----------------------

try: 
    # Check if DB_HOSTNAME is provided
    DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
    assert DB_HOSTNAME, "DB_HOSTNAME environment variable is not set."

    # Check if DB_NAME is provided
    DB_NAME = os.environ.get("DB_NAME")
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
    error_file_path = os.path.join(constants.PATH_TO_ROOT, "logs", "logs.error")
    utils.log(f"Location Short Title: {constants.LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)


# ----------------------- DATABASE CONNECTION -----------------------
def connect_to_db():
    # Try to connect 10 times - exponential backoff
    for i in range(10):
        try: 
            db_connection = psycopg2.connect(
                host = DB_HOSTNAME, 
                dbname = DB_NAME, 
                user = DB_USERNAME, 
                password = DB_PASSWORD, 
                port = DB_PORT
            )
            if db_connection.closed == 0: 
                utils.log("Successful establlished connection to db.", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
                return db_connection  # singleton? 
            else: 
                utils.log(f"Connection failed, sleep {pow(2, i)} seconds.", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
                # sleep and retry later again.
                time.sleep(pow(2, i))
        # failed
        except psycopg2.Error as e:
            utils.log(f"Error connecting to the database: {str(e)}", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
            # sleep and retry later again.
            time.sleep(2**i)
