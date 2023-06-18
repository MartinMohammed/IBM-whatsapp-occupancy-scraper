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
class DBTest(TestCase):

    @patch("time.sleep")
    def test_db_connect_if_db_exists(self, *args):
        """
        Test the connection to the database.

        The function performs the following steps:
        - Mocks the necessary objects and methods.
        - Sets up the side effects for the patched_connect function to simulate connection failures and success.
        - Calls the connect_to_db function.
        - Verifies that the patched_connect method is called with the expected parameters.
        - Verifies that the cursor and execute methods are called.
        - Verifies the return value of connect_to_db.
        """




        # Assert that the patched_connect method was called exactly once with the expected parameters
        patched_connect = args[1]
        patched_check_if_db_exists = args[3]

        # mocks
        mocked_connection = MagicMock()
        mocked_cursor = MagicMock()

        mocked_connection.cursor = mocked_cursor
        mocked_connection.closed = 0  # indicate that the connection attempt has succeeded

        patched_connect.return_value = mocked_connection

        # Db already exists. 
        patched_check_if_db_exists.return_value = True

        mocked_connection_return_value = connect_to_db()

        # Just make sure the psycopg2.connect() method was called 
        # with the right parameters.
        patched_connect.assert_called_once_with(
            host=os.getenv("DB_HOSTNAME"),
            dbname="postgres",
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

   

        # ------------------ EXPECT NO DB WILL BE CREATED ------------------
        mocked_cursor.return_value.assert_not_called()
        mocked_connection.commit.assert_not_called()
        # ------------------ EXPECT NO DB WILL BE CREATED ------------------

        # Expect that the method returns the established connection.
        self.assertEqual(mocked_connection_return_value, mocked_connection)

    @patch("time.sleep")
    def test_db_connect_if_db_not_exists(self, *args):
        """
        Test the connection to the database.

        The function performs the following steps:
        - Mocks the necessary objects and methods.
        - Sets up the side effects for the patched_connect function to simulate connection failures and success.
        - Calls the connect_to_db function.
        - Verifies that the patched_connect method is called with the expected parameters.
        - Verifies that the cursor and execute methods are called.
        - Verifies the return value of connect_to_db.
        """

        


        # Assert that the patched_connect method was called exactly once with the expected parameters
        patched_connect = args[1]
        patched_check_if_db_exists = args[3]

        # mocks
        mocked_connection = MagicMock()
        mocked_cursor = MagicMock()

        mocked_connection.cursor = mocked_cursor
        mocked_connection.closed = 0  # indicate that the connection attempt has succeeded

        patched_connect.return_value = mocked_connection

        # Db does not already exist. 
        patched_check_if_db_exists.return_value = False


        mocked_connection_return_value = connect_to_db()

        # Just make sure the psycopg2.connect() method was called 
        # with the right parameters.
        patched_connect.assert_called_once_with(
            host=os.getenv("DB_HOSTNAME"),
            dbname="postgres",
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

        # ------------------ EXPECT  DB WILL BE CREATED ------------------
        db_name = os.getenv("DB_NAME")
        mocked_cursor.return_value.execute.assert_called_once_with(f"CREATE DATABASE {db_name}")
        mocked_connection.commit.assert_called()
        # ------------------ EXPECT DB WILL BE CREATED ------------------
        # Expect that the method returns the established connection.
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

        # The side_effect attribute of a mock object allows you to define the behavior when the patched_connect function is called.
        # In this case, it will raise psycopg2.DatabaseError once and then return the mock_instance.
        side_effects = [psycopg2.DatabaseError] + [psycopg2.Error] + [connection_mock_closed] + [connection_mock_opened]
        patched_connect.side_effect = side_effects


        # --------------- CHECK IF DB EXISTS SHOULD BE SKIPPED (does already exist)  --------------- #
        patched_check_if_db_exists.return_value = True        
        # --------------- CHECK IF DB EXISTS SHOULD BE SKIPPED  --------------- #

        connect_to_db()
        
        # Expect that sys.exit() is called with the appropriate error code when a DatabaseError occurs
        patched_sys_exit.assert_called_once_with(1) 

        # Expect that the log function is called with the expected message
        db_name = os.getenv("DB_NAME")
        patched_log.assert_called_with(f"Database {db_name} does already exist.", file_path=os.path.join(constants.LOG_DIRECTORY, "db.log"))

        # Assert that the log function was called 5 times
        self.assertEqual(patched_log.call_count, 5)

        # Assert that the patched_connect function was called the expected number of times
        self.assertEqual(patched_connect.call_count, len(side_effects))


        # Assert that the patched_sleep function was called the expected number of times
        self.assertEqual(patched_sleep.call_count, len(side_effects) - 2)
