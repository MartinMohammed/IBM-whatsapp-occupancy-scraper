import os
import requests
from datetime import datetime
import csv
from . import constants

def fetch_data(url: str) -> dict:
    """
    Make an API request to fetch studio data.

    Args:
        url (str): The URL of the API endpoint.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.HTTPError: If an HTTP error occurs during the request.
    """
    try:
        response = requests.get(url=url, headers={'Accept': 'application/json'})
        response.raise_for_status()
    except requests.HTTPError as e:
        log(file_path=os.path.join(os.getcwd(), "logs", "requests.log"), message=str(e))
    return response.json()


def write_to_csv(file_path: str, header: list, *args):
    """
    Write data to a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        header (list): The header row for the CSV file.
        *args: Variable number of arguments representing the data rows.

    Note:
        The CSV file is opened in append mode.

    """
    with open(file_path, mode="a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        if os.path.getsize(filename=file_path) == 0:
            csv_writer.writerow(header)
        csv_writer.writerow(args)


def log(message: str, file_path: str = None):
    """
    Write a log message to a file or print it to the console.

    Args:
        file_path (str): The path to the log file. If None, the message will be printed to the console.
        message (str): The log message to write.

    Note:
        If file_path is provided, the log file is opened in append mode and the log message is printed to the console.
        If file_path is None, the log message is printed to the console.
    """

    timestamp = datetime.now().strftime('%d-%m-%Y-%H-%M')
    log_message = f"Timestamp {timestamp}: {message}"

    if file_path is not None:
        with open(file_path, mode="a", encoding="utf-8") as file:
            file.write(log_message)
            file.write("\n")

       
    print(log_message)
    print("_" * 50)
        


def check_is_week_day(current_day: int) -> bool:
    """
    Checks if today is a weekday (Monday including Friday) or not.

    Args:
        current_day (int): The current day represented as an integer (0 = Monday, 1 = Tuesday, ...).

    Returns:
        bool: True if it is a weekday, False otherwise.
    """
    if (not (0 <= current_day <= 6)):
        log("Warning: Provided weekday is not valid.")
        current_day = datetime().now().weekday()

    return 0 <= current_day <= 4

def check_if_in_opening_hours(current_time: int, is_week_day: bool) -> bool:
    """
    Checks if the current time falls within the opening hours of the studio.

    Args:
        current_time (int): The current time represented as an integer (24-hour format).
        is_week_day (bool): A boolean indicating whether it is a weekday or weekend.

    Returns:
        bool: True if the current time falls within the opening hours, False otherwise.
    """
    opening_hours = constants.OPENING_HOURS["week_day" if is_week_day else "week_end"]
    studio_open = opening_hours.get("open")
    studio_close = opening_hours.get("close")

    return (studio_open <= current_time < studio_close)

def construct_file_name(date: datetime, location_short_title: str) -> str:
    """
    Constructs a file name for storing visitor data.

    Args:
        date (datetime): The current date and time.
        location_short_title (str): The short title of the location.

    Returns:
        str: The constructed file name.
    """
    timestamp = date.strftime("%d-%m-%Y-%H-%M")

    # Generate a new filename with the timestamp
    return f"visitors-{location_short_title}-{timestamp}.csv"

def calculate_sleep_time_in_seconds(date: datetime, opening_hour: int, tomorrow = True):
    # Calculate the number of hours to sleep until the next day's opening time
    # Example: If the current time is 23:34 and the opening time for tomorrow is exactly at 8 AM,
    # the calculation would be: 24 - (23 + 1) = 0 hours until tomorrow (excluding the next day's opening hour)
    # Additionally, 60 - 34 = 26 minutes until tomorrow (excluding the next day's opening hour)
    # Therefore, the total hours to sleep until tomorrow would be (8 + 0) hours and 26 minutes, which is 506 minutes.

    hours_to_sleep = opening_hour + (24 - (date.hour + 1)) 
    if not tomorrow:
        # today: 
        hours_to_sleep = opening_hour - 1
    
    # Calculate the number of minutes to sleep, accounting for the missing minutes in the previous calculation
    # Example: If the current time is 23:34, there are 60 minutes in an hour, so the minutes until the next hour would be 26.

    minutes_to_sleep = 60 - (date.minute + 1)
    
    # Calculate the total number of minutes to sleep
    # Example: If the hours to sleep is 2 and the minutes to sleep is 26, the total minutes to sleep would be:
    # 2 * 60 + 26 = 146 minutes until tomorrow
    total_minutes_to_sleep = (hours_to_sleep * 60) + minutes_to_sleep
    
    seconds_to_sleep = 60 - date.second

    # Convert the total minutes to sleep to seconds
    # Example: If the total minutes to sleep is 146, to convert it to seconds, we multiply by 60:
    # 146 * 60 = 8760 seconds until tomorrow
    sleep_time_in_seconds = (total_minutes_to_sleep * 60) + seconds_to_sleep
    
    return sleep_time_in_seconds
