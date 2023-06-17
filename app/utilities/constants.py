"""Constant values such as settings from e.g. inferred from environment."""
import os
import sys
from . import utils_log


# /app inside docker container.
PATH_TO_ROOT = os.getcwd()
DATA_DIRECTORY = os.path.join(PATH_TO_ROOT, "data") 
# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

# Create the data directory if it doesn't exist
LOG_DIRECTORY = os.path.join(PATH_TO_ROOT, "logs")
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

OPENING_HOURS = {
        "FFGR": {
            # MON including FRI
            "week_day": {"open": 8, "close": 23},
            # SAT including SUN
            "week_end": {"open": 8, "close": 21}
        }, 
        "FFDA": {
            # MON including FRI
            "week_day": {"open": 8, "close": 23},
            # SAT including SUN
            "week_end": {"open": 10, "close": 21}
        }, 
        "FFHB": {
             # MON including FRI
            "week_day": {"open": 0, "close": 24},
            # SAT including SUN
            "week_end": {"open": 0, "close": 24}
        }
}.get(os.getenv("LOCATION_SHORT_TITLE"))


# ----------------------- SETTINGS -----------------------
REQUEST_DENSITY = 60 * int(os.getenv("REQUEST_DENSITY") or 5)  # Specifies the frequency of API requests in seconds.
ENTRIES_UNTIL_FILE_SEGMENTATION = int(os.getenv("ENTRIES_UNTIL_FILE_SEGMENTATION") or 1000)  # How many entries in the CSV file until a new one is created.

# Required Environment variables:
try:
    assert isinstance(REQUEST_DENSITY, int), "REQUEST_DENSITY must be a valid integer."
    assert isinstance(ENTRIES_UNTIL_FILE_SEGMENTATION, int), "ENTRIES_UNTIL_FILE_SEGMENTATION must be a valid integer."

    LOCATION_ID = os.getenv("LOCATION_ID")  # The ID of the gym location.
    assert LOCATION_ID is not None, "LOCATION_ID was not provided."

    LOCATION_SHORT_TITLE = os.getenv("LOCATION_SHORT_TITLE")  # Indicates the location to be tracked based on the gym-mapping.json file.
    assert LOCATION_SHORT_TITLE is not None, "LOCATION_SHORT_TITLE was not provided."

    URL = os.getenv("API_URL")
    assert URL is not None, "API_URL was not provided."

    LOCATION_ID = int(LOCATION_ID)
except AssertionError as e:
    error_file_path = os.path.join(LOG_DIRECTORY, "logs.error")
    utils_log.log(f"Location Short Title: {LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)

# ----------------------- SETTINGS -----------------------
