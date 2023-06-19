import os
import requests
from datetime import datetime
from . import constants
from . import utils_log

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
        utils_log.log(file_path=os.path.join(constants.LOCATION_LOG_DIR, "requests.log"), message=str(e))
    return response.json()

def check_is_week_day(current_day: int) -> bool:
    """
    Check if today is a weekday (Monday to Friday) or not.

    Args:
        current_day (int): The current day represented as an integer (0 = Monday, 1 = Tuesday, ...).

    Returns:
        bool: True if it is a weekday, False otherwise.
    """
    if not (0 <= current_day <= 6):
        utils_log.log("Warning: The provided weekday is not valid.")
        current_day = datetime.now().weekday()

    return 0 <= current_day <= 4

def check_if_in_opening_hours(current_time: int, is_week_day: bool) -> bool:
    """
    Check if the current time falls within the opening hours of the studio.

    Args:
        current_time (int): The current time represented as an integer (24-hour format).
        is_week_day (bool): A boolean indicating whether it is a weekday or weekend.

    Returns:
        bool: True if the current time falls within the opening hours, False otherwise.
    """
    opening_hours = constants.OPENING_HOURS["week_day" if is_week_day else "week_end"]
    studio_open = opening_hours.get("open")
    studio_close = opening_hours.get("close")

    return studio_open <= current_time < studio_close

def get_today_visitors_file_name_if_it_does_exist(year: int, month: int, day: int):
    """
    Check if the visitors file for the provided month and day exists in the current directory.
    """
    # e.g. fixed pattern: 
    # day: index 14 start
    # visitors-FFGR-17-06-2023-20-00.csv
    day = f"0{day}" if day < 10 else str(day)
    month = f"0{month}" if month < 10 else str(month)
    year = str(year)

    file_names = os.listdir(constants.LOCATION_DATA_DIR)
    for file_name in file_names:
        # (16 not included)
        split_file_name = file_name.split("-")

        file_name_day = split_file_name[2]
        file_name_month = split_file_name[3]
        file_name_year = split_file_name[4]

        utils_log.log(file_name)
        if file_name_day == day and file_name_month == month and file_name_year == year:
            utils_log.log(f"Found an existing file, continue writing there: {file_name}.")
            return file_name

    # No match found
    utils_log.log(f"Did not find an existing file for day: {day}, month: {month}, {year}, create a new file.")
    return None 

def construct_visitor_file_name(date: datetime) -> str:
    """
    Construct a file name for storing visitor data.

    Args:
        date (datetime): The current date and time.

    Returns:
        str: The constructed file name.
    """
    timestamp = date.strftime("%d-%m-%Y-%H-%M")

    # Generate a new filename with the timestamp
    return f"visitors-{constants.LOCATION_SHORT_TITLE}-{timestamp}.csv"

def calculate_sleep_time_in_seconds(date: datetime, opening_hour: int):
    """
    Calculate the number of seconds to sleep until the next day's opening time.

    Args:
        date (datetime): The current date and time.
        opening_hour (int): The hour representing the opening time of the next day.

    Returns:
        int: The number of seconds to sleep until the next day's opening time.
    """
    # Determine if it is tomorrow based on the current time and the opening hour
    tomorrow = date.hour >= opening_hour

    # Calculate the number of hours to sleep until the next day's opening time
    hours_to_sleep = opening_hour + (24 - (date.hour + 1))
    if not tomorrow:
        # If it's not tomorrow, adjust the hours to sleep
        # Calculate the time until it is opening hours
        # e.g. opens at 8am, and it is not 3:34 am 
        # 8 - 4 =  hours until 7:34
        hours_to_sleep = opening_hour - (date.hour + 1)
    
    # Calculate the number of minutes to sleep, accounting for the missing minutes in the previous calculation
    minutes_to_sleep = 60 - (date.minute + 1)
    
    # Calculate the total number of minutes to sleep
    total_minutes_to_sleep = (hours_to_sleep * 60) + minutes_to_sleep
    
    # Calculate the number of seconds to sleep, accounting for the missing seconds in the previous calculation
    seconds_to_sleep = 60 - date.second

    # Convert the total minutes to sleep to seconds
    sleep_time_in_seconds = (total_minutes_to_sleep * 60) + seconds_to_sleep
    
    return sleep_time_in_seconds
