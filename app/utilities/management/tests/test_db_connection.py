from unittest import TestCase
from unittest.mock import patch, MagicMock
import os
import psycopg2
from ..db_connect import connect_to_db
@patch("utilities.utils.log")
@patch("builtins.print")
@patch("psycopg2.connect")
class DBTest(TestCase):


    @patch("time.sleep")
    def test_db_connect(self, patched_sleep, patched_connect, patched_print, patched_log):
        """
        Test that connect_to_db calls the patched_connect method with certain parameters to connect to the database.
        """

        connect_to_db()

        # Assert that the patched_connect method was called exactly once with the expected parameters
        patched_connect.assert_called_with(
            host=os.environ.get("DB_HOSTNAME"),
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT")
        )

        # Create a MagicMock instance to mock the database connection object
        mock_connection_instance = MagicMock()
        mock_connection_instance.closed = 0
        patched_connect.return_value = mock_connection_instance

        # Assert that the patched_connect method was called at least once
        patched_connect.assert_called()

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_connect, patched_print, patched_log):
        """
        Test the exponential backoff when the database is not online.
        """

        # Create MagicMock instances to mock the original connection instances
        mock_instance1 = MagicMock()
        mock_instance1.closed = 1

        mock_instance2 = MagicMock()
        mock_instance2.closed = 0

        # The side_effect attribute of a mock object allows you to define the behavior when the patched_connect function is called.
        # In this case, it will raise psycopg2.Error once and then return the mock_instance.
        patched_connect.side_effect = [psycopg2.Error] + [mock_instance1] + [mock_instance2]
        
        connect_to_db()

        # Assert that the patched_log method was called 3 times
        self.assertEqual(patched_log.call_count, 3)

        # Assert that the patched_connect method was called 3 times (1 error + 2 successful connections)
        self.assertEqual(patched_connect.call_count, 3)

        # Assert that the patched_sleep method was called twice (for the 2 sleep calls in the function)
        self.assertEqual(patched_sleep.call_count, 2)
