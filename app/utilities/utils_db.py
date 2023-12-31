import os
from . import utils_log
from . import constants

"""Utilities related to working with PostgreSQL database."""

def create_table_if_not_exists(connection, table_name, fields):
    """
    Create a table with the specified table name and fields.

    Args:
        connection (psycopg2.extensions.connection): The database connection.
        table_name (str): The name of the table to create.
        fields (str): The fields and their data types for the table.

    Example:
        create_table_if_not_exists(connection, 'employee', '''
            (
                EmployeeID int, 
                name varchar(40) NOT NULL, 
                salary int, 
                dept_id varchar(30)
            )
        ''')
    """
    with connection.cursor() as cursor:
        query = f'''CREATE TABLE IF NOT EXISTS {table_name}{fields}'''
        cursor.execute(query)
        utils_log.log("Creating a new table if it doesn't exist.", os.path.join(constants.LOCATION_LOG_DIR, "db.log"))
        connection.commit()

def save_to_db(connection, table_name, fields, values):
    """
    Save entries to the specified table with the given values.

    Args:
        connection (psycopg2.extensions.connection): The database connection.
        table_name (str): The name of the table to insert the values into.
        values (tuple): The values to be inserted into the table.

    Example:
        save_to_db(connection, 'employee', (1, "John", 50000, 'D1'))
    """
    # Use a context manager to automatically close the cursor after execution
    with connection.cursor() as cursor:
        # Note: 
        # When you pass an integer value as a parameter using %s in a formatted string and then save it to the database,
        # the integer value will be properly stored in the corresponding integer column in the database.
        query = f"INSERT INTO {table_name} {fields} VALUES(%s, %s)"
        cursor.execute(query, values)
        connection.commit()
        utils_log.log(f"Successfully saved data into {table_name} with fields: '${fields}'.", os.path.join(constants.LOCATION_LOG_DIR, "db.log"))

def check_if_database_exists(db_connection, db_name: str) -> bool:
    """
    Check if the specific database already exists in the PostgreSQL instance.

    :param db_connection: PostgreSQL database connection object.
    :param db_name: Name of the database to check.
    :return: True if the database exists, False otherwise.
    """
    
    # Construct the query to check if the database exists
    query = f"SELECT datname FROM pg_database WHERE datname = '{db_name.replace('-', '_')}';"
    
    # Create a cursor object to execute the query
    cursor = db_connection.cursor()
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch the result (one row)
    db_does_exist = cursor.fetchone()
    
    # Close the cursor
    cursor.close()
    
    # Return True if a row is fetched (database exists), False otherwise
    return True if db_does_exist else False
