from unittest import (TestCase, mock)
from .. import utils_db

@mock.patch("builtins.print")
class TestDBUtils(TestCase):
    """Tests related to DB tools"""

    # --------------------- FOR DATABASE --------------------- #
    def test_create_table_if_not_exists(self, patched_print):
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


    def test_save_to_db(self, patched_print):
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

        utils_db.save_to_db(connection=mock_connection, table_name=table_name, values=(timestamp, visitor_count))
        expected_query = f"INSERT INTO {table_name} (timestamp, visitor_count) VALUES(%s, %s)"

        # Check if cursor.execute has correct constructed query in order to insert
        mock_cursor.execute.assert_called_once_with(expected_query, (timestamp, visitor_count))

        # Check if connection.commit() was called once.
        mock_connection.commit.assert_called_once()


