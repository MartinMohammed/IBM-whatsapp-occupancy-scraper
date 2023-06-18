from unittest import (TestCase, mock)
import os
from .. import utils_db

@mock.patch("utilities.utils_log.log")
@mock.patch("builtins.print")
class TestDBUtils(TestCase):
    """Tests related to DB tools"""

    # --------------------- FOR DATABASE --------------------- #
    def test_create_table_if_not_exists(self, *args):
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

        table_name = "visitors-FFGR"
        fields = "(timestamp TIMESTAMP, visitor_count INT)"
        utils_db.create_table_if_not_exists(connection=mock_connection, table_name=table_name, fields=fields)

        # Check if the execute method was called with the correct arguments
        expected_query = f"CREATE TABLE IF NOT EXISTS {table_name}{fields}"
        mock_cursor.execute.assert_called_once_with(expected_query)

        # Check if connection commit method was called
        mock_connection.commit.assert_called_once()


    def test_save_to_db(self, *args):
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

        fields = "(timestamp TIMESTAMP, visitor_count INT)"
        utils_db.save_to_db(connection=mock_connection, fields=fields, table_name=table_name, values=(timestamp, visitor_count))
        expected_query = f"INSERT INTO {table_name} {fields} VALUES(%s, %s)"

        # Check if cursor.execute has correct constructed query in order to insert
        mock_cursor.execute.assert_called_once_with(expected_query, (timestamp, visitor_count))

        # Check if connection.commit() was called once.
        mock_connection.commit.assert_called_once()
    
    
    def test_check_if_database_exists_true(self, *args):
        """
        Test if a specific database already exists when it does exist.

        The function performs the following steps:
        - Creates mocked instances for the database connection and cursor.
        - Sets up the expected query and fetchone result to simulate the existence of the database.
        - Calls the `check_if_database_exists` function.
        - Verifies that the cursor, execute, fetchone, and close methods are called with the expected arguments.
        - Asserts that the database existence is correctly identified as True.
        """

        # Create mocked instances for the database connection and cursor
        mocked_connection = mock.MagicMock()
        mocked_cursor = mock.MagicMock()

        mocked_connection.cursor = mocked_cursor

        db_name = os.getenv("DB_NAME")

        # Set the fetchone result to True, indicating that the database exists for this test
        mocked_cursor.fetchone.return_value = True

        # Call the check_if_database_exists function
        does_exist = utils_db.check_if_database_exists(db_connection=mocked_connection, db_name=db_name)

        # Set up the expected query
        expected_query = f"SELECT datname FROM pg_database WHERE datname = '{db_name}';"

        # Check if the cursor was called to create a cursor
        mocked_cursor.assert_called_once()

        # Check if the query was executed on the cursor
        mocked_cursor.execute.assert_called_once_with(expected_query)

        # Check if the result was fetched from the cursor
        mocked_cursor.fetchone.assert_called_once()

        # Check if the cursor was closed appropriately
        mocked_cursor.close.assert_called_once()

        # Assert that the database existence is correctly identified as True
        self.assertTrue(does_exist)





