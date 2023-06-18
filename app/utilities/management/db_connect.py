# db_connect.py
"""Module for doing some setup like connecting to an DB."""
import os 
import sys
import time
import psycopg2
from .. import utils_log
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
    utils_log.log(f"Location Short Title: {constants.LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)


# ----------------------- DATABASE CONNECTION -----------------------
def connect_to_db():
    # Try to connect 10 times - exponential backoff
    retry_delay = 1
    retries = 10
    for attempt in range(retries):
        try: 
            db_connection = psycopg2.connect(
                host = DB_HOSTNAME, 
                # default db name. 
                dbname = "postgres", 
                user = DB_USERNAME, 
                password = DB_PASSWORD, 
                port = DB_PORT
            )
            connection_succeed = db_connection.closed == 0
            if connection_succeed: 
                utils_log.log("Successful establlished connection to db.", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))

                # # Now create a new database if not exists 
                # db_connection.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
                # db_connection.commit()

                # utils_log.log("Successful created database table if it not exists before.", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))

                return db_connection  # singleton? 
            else: 
                utils_log.log(f"Connection failed, sleeping for {retry_delay} seconds.", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
                # sleep and retry later again.
                time.sleep(retry_delay)
                retry_delay *= 2 # exponential backoff

        except psycopg2.DatabaseError as e:
            utils_log.log(f"Error creating database {DB_NAME}: {str(e)}", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
            sys.exit(1) # database creation failed -> cannot continue!
            
        except psycopg2.Error as e:
            utils_log.log(f"Error connecting to the database (sleep {retry_delay} seconds.): {str(e)}", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
            time.sleep(retry_delay) # database connection attempt failed -> sleep and retry later again.

    utils_log.log(f"Failed to establish a database connection after multiple {retries} attempts.",
                  file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))
    sys.exit(1)

