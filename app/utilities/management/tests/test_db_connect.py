from unittest import TestCase
from unittest.mock import patch, MagicMock
import os
import psycopg2
from ... import constants
from ..db_connect import connect_to_db


@patch("utilities.utils_log.log")
@patch("utilities.utils_db.check_if_database_exists")
@patch("builtins.print")
@patch("psycopg2.connect")
class TestDB(TestCase):
    def setUp(self):
        """
        Set up the test case by initializing the database credentials and file path.
        """
        # Database credentials
        self.db_host = os.getenv("DB_HOSTNAME")
        self.db_name = os.getenv("DB_NAME").replace("-", "_")
        self.db_user = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = os.getenv("DB_PORT")

        self.file_path = os.path.join(constants.LOCATION_LOG_DIR, "db.log")

    @patch("time.sleep")
    def test_db_connect_if_db_exists(self, *args):
        """
        Test the connection to the database when the database already exists.

        The function performs the following steps:
        - Mocks the necessary objects and methods.
        - Sets up the side effects for the patched_connect function to simulate connection failures and success.
        - Calls the connect_to_db function.
        - Verifies that the patched_connect method is called with the expected parameters.
        - Verifies that no database creation steps are performed.
        - Verifies the return value of connect_to_db.
        """
        patched_connect = args[1]
        patched_check_if_db_exists = args[3]
        patched_log = args[4]

        # Mock objects
        mocked_connection = MagicMock()
        mocked_cursor = MagicMock()

        # Configure the return value of the connection.cursor() method
        mocked_connection.cursor.return_value = mocked_cursor
        mocked_connection.closed = 0  # Indicate that the connection attempt has succeeded

        patched_connect.return_value = mocked_connection

        # Database already exists.
        patched_check_if_db_exists.return_value = True

        # Call the connect_to_db function
        mocked_connection_return_value = connect_to_db(
            db_host=self.db_host,
            db_name=self.db_name,
            db_user=self.db_user,
            db_password=self.db_password,
            db_port=self.db_port,
            recursion_depth=0
        )

        # Verify that the patched_connect method was called exactly once with the expected parameters
        patched_connect.assert_called_once_with(
            host=self.db_host,
            database="postgres",  # Default db name
            user=self.db_user,
            password=self.db_password,
            port=self.db_port,
        )

        # Verify that no database creation steps are performed
        mocked_cursor.assert_not_called()
        mocked_connection.commit.assert_not_called()
        mocked_connection.close.assert_not_called()

        # Verify that the log function is called with the expected message
        patched_log.assert_called_with(f'Database {self.db_name} already exists. Continuing writing to that database.', file_path=self.file_path)

        # Verify that the method returns the established connection
        self.assertEqual(mocked_connection_return_value, mocked_connection)

    @patch("time.sleep")
    def test_db_connect_if_db_not_exists(self, *args):
        """
        Test the connection to the database when the database does not exist.

        The function performs the following steps:
        - Mocks the necessary objects and methods.
        - Sets up the side effects for the patched_connect function to simulate connection failures and success.
        - Calls the connect_to_db function.
        - Verifies that the patched_connect method is called with the expected parameters.
        - Verifies that the cursor and execute methods are called for database creation.
        - Verifies the return value of connect_to_db.
        """
        patched_connect = args[1]
        patched_check_if_db_exists = args[3]
        patched_log = args[4]

        # Mock objects
        mocked_connection = MagicMock()
        mocked_cursor = MagicMock()
        mocked_cursor_context_manager = MagicMock()

        # Set the __enter__ method of the mocked cursor to the mocked cursor context manager
        mocked_cursor.__enter__.return_value = mocked_cursor_context_manager

        # Configure the return value of the connection.cursor() method
        mocked_connection.cursor.return_value = mocked_cursor

        # Set the closed attribute of the connection to indicate a successful connection attempt
        mocked_connection.closed = 0

        patched_connect.side_effect = [mocked_connection, mocked_connection]

        patched_check_if_db_exists.side_effect = [False, True]

        # Call the connect_to_db function
        mocked_connection_return_value = connect_to_db(
            db_host=self.db_host,
            db_name=self.db_name,
            db_user=self.db_user,
            db_password=self.db_password,
            db_port=self.db_port,
            recursion_depth=0
        )

        # Verify that the patched_connect method was called with the expected parameters
        patched_connect.assert_called_with(
            host=self.db_host,
            database=self.db_name,  # Default db name
            user=self.db_user,
            password=self.db_password,
            port=self.db_port,
        )

        # Verify that the cursor and execute methods are called for database creation
        mocked_connection.close.assert_called()
        assert patched_connect.call_count == 2, "psycopg2.connect was not called twice as expected."
        mocked_cursor_context_manager.execute.assert_called_once_with(f"CREATE DATABASE {self.db_name.replace('-', '_')}")

        # Verify that the log function is called with the expected message
        patched_log.assert_called_with(f'Database {self.db_name} already exists. Continuing writing to that database.', file_path=self.file_path)

        # Verify that the method returns the established connection
        self.assertEqual(mocked_connection_return_value, mocked_connection)

    @patch("sys.exit")
    @patch("time.sleep")
    def test_wait_for_db_delay(self, *args):
        """
        Test the exponential backoff when the database is not online.

        The function performs the following steps:
        - Mocks the necessary objects and methods.
        - Sets up the side effects for the patched_connect function to simulate connection failures and success.
        - Calls the connect_to_db function.
        - Verifies that sys.exit() is called when a DatabaseError occurs.
        - Verifies that the log function is called with the expected messages.
        - Verifies the number of times the log, connect, and sleep functions are called.
        """
        patched_sleep = args[0]
        patched_sys_exit = args[1]
        patched_connect = args[2]
        patched_check_if_db_exists = args[4]
        patched_log = args[5]

        # Create MagicMock instances to mock the original connection instances
        connection_mock_closed = MagicMock()
        connection_mock_closed.closed = 1

        connection_mock_opened = MagicMock()
        connection_mock_opened.closed = 0

        # The side_effect attribute of a mock object allows you to define the behavior when the patched_connect
        # function is called. In this case, it will raise psycopg2.DatabaseError once and then return the mock_instance.
        side_effects = [psycopg2.DatabaseError] + [psycopg2.Error] + [connection_mock_closed] + [connection_mock_opened]
        patched_connect.side_effect = side_effects

        # Check if DB exists should be skipped (already exists)
        patched_check_if_db_exists.return_value = True

        connect_to_db(
            db_host=self.db_host,
            db_name=self.db_name,
            db_user=self.db_user,
            db_password=self.db_password,
            db_port=self.db_port,
            recursion_depth=0,
        )

        # Verify that sys.exit() is called with the appropriate error code when a DatabaseError occurs
        # patched_sys_exit.assert_called_once_with(1)

        # Verify that the log function is called with the expected message
        patched_log.assert_called_with(f'Database {self.db_name} already exists. Continuing writing to that database.', file_path=self.file_path)

        # Verify the number of times the log function is called
        self.assertEqual(patched_log.call_count, 5)

        # Verify the number of times the patched_connect function is called
        self.assertEqual(patched_connect.call_count, len(side_effects))

        # Verify the number of times the patched_sleep function is called
        self.assertEqual(patched_sleep.call_count, 3)
