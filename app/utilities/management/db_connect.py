# db_connect.py
"""Module for setting up the database connection."""

import os
import sys
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .. import utils_log, utils_db
from .. import constants


def connect_to_db(db_host, db_name, db_user, db_password, db_port, recursion_depth=0):
    """
    Connects to the database.

    Args:
        db_host (str): The hostname of the database server.
        db_name (str): The name of the database.
        db_user (str): The username for connecting to the database.
        db_password (str): The password for connecting to the database.
        db_port (int): The port number for the database server.
        recursion_depth (int, optional): The recursion depth for creating a new database. Defaults to 0.

    Returns:
        psycopg2.extensions.connection: The database connection.

    Raises:
        SystemExit: If the database connection cannot be established.
    """

    # Try to connect 10 times - exponential backoff
    retry_delay = 1
    retries = 10
    db_log_file_path = os.path.join(constants.LOCATION_LOG_DIR, "db.log")

    # Default database name is guaranteed to exist.
    for attempt in range(retries):
        try:
            # Initial connection
            db_connection = psycopg2.connect(
                host=db_host,
                database="postgres" if recursion_depth == 0 else db_name,
                user=db_user,
                password=db_password,
                port=db_port
            )
            connection_succeed = db_connection.closed == 0
            if connection_succeed:
                utils_log.log("Successfully established a connection to the database.", file_path=db_log_file_path)

                # Now create a new database if it doesn't exist
                database_does_not_exist = not utils_db.check_if_database_exists(db_connection=db_connection, db_name=db_name)
                if database_does_not_exist:
                    db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

                    # Obtain a database cursor
                    with db_connection.cursor() as cursor:
                        # Create a new database
                        cursor.execute(f"CREATE DATABASE {db_name.replace('-', '_')}")

                        db_connection.autocommit = False

                        # Close the connection and establish a new one
                        db_connection.close()

                        # The database now exists, create a new connection to the newly created database
                        utils_log.log(f"Successfully created database {db_name}.", file_path=db_log_file_path)

                        # Recursive call to connect to the new database
                        return connect_to_db(
                            db_host=db_host,
                            db_name=db_name,
                            db_user=db_user,
                            db_password=db_password,
                            db_port=db_port,
                            recursion_depth=recursion_depth + 1
                        )
                else:
                    utils_log.log(f"Database {db_name} already exists. Continuing writing to that database.", file_path=db_log_file_path)
                    db_connection.close()

                    # Return connection to already existing database. 
                    new_connection =  psycopg2.connect(
                        host=db_host,
                        database=db_name,
                        user=db_user,
                        password=db_password,
                        port=db_port
                    )
                    return new_connection

            else:
                utils_log.log(f"Connection failed. Sleeping for {retry_delay} seconds.", file_path=db_log_file_path)
                # Sleep and retry later
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff

        except psycopg2.DatabaseError as e:
            utils_log.log(f"Error creating database {db_name}: {str(e)}", file_path=db_log_file_path)
            retry_delay *= 2  # Exponential backoff
            time.sleep(retry_delay)  # Database connection attempt failed, sleep and retry later

        except psycopg2.Error as e:
            utils_log.log(f"Error connecting to the database (sleep {retry_delay} seconds.): {str(e)}", file_path=db_log_file_path)
            retry_delay *= 2  # Exponential backoff
            time.sleep(retry_delay)  # Database connection attempt failed, sleep and retry later

    utils_log.log(f"Failed to establish a database connection after {retries} attempts.", file_path=db_log_file_path)
    sys.exit(1)
