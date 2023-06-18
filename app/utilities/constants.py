import os
import sys
from . import utils_log


# Constant values such as settings inferred from environment.

# /app inside docker container.
PATH_TO_ROOT = os.getcwd()

# Create the data directory if it doesn't exist.
DATA_DIRECTORY = os.path.join(PATH_TO_ROOT, "data")
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

# Create the log directory if it doesn't exist.
LOG_DIRECTORY = os.path.join(PATH_TO_ROOT, "logs")
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)


# ----------------------- SETTINGS -----------------------
# Frequency of API requests in seconds.
try:
    REQUEST_DENSITY = int(os.getenv("REQUEST_DENSITY", 5)) * 60
except ValueError:
    REQUEST_DENSITY = 5 * 60  # Use a default value of 5 minutes

# How many entries in the CSV file until a new one is created.
try:
    ENTRIES_UNTIL_FILE_SEGMENTATION = int(os.getenv("ENTRIES_UNTIL_FILE_SEGMENTATION", 1000))
except ValueError:
    ENTRIES_UNTIL_FILE_SEGMENTATION = 1000  # Use a default value of 1000


# Required Environment variables:
try:
    assert isinstance(REQUEST_DENSITY, int), "REQUEST_DENSITY must be a valid integer."
    assert isinstance(ENTRIES_UNTIL_FILE_SEGMENTATION, int), "ENTRIES_UNTIL_FILE_SEGMENTATION must be a valid integer."

    LOCATION_SHORT_TITLE = os.getenv("LOCATION_SHORT_TITLE")  # Indicates the location to be tracked based on the gym-mapping.json file.
    assert LOCATION_SHORT_TITLE is not None, "LOCATION_SHORT_TITLE was not provided."

except AssertionError as e:
    error_file_path = os.path.join(LOG_DIRECTORY, "logs.error")
    utils_log.log(f"Location Short Title: {LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)

# ----------------------- SETTINGS -----------------------


# Studios are identified by their LOCATION SHORT NAME:
STUDIO_MAP = {
    "FFDA": {
        "id": "1",
        "title": "Fitness Fabrik Darmstadt",
        "opening_hours": {
            # MON including FRI
            "week_day": {"open": 8, "close": 23},
            # SAT including SUN
            "week_end": {"open": 10, "close": 21}
        }
    },
    "FFHB": {
        "id": "2",
        "title": "Fitness Fabrik Darmstadt (Hbf)",
        "opening_hours": {
            # MON including FRI
            "week_day": {"open": 0, "close": 24},
            # SAT including SUN
            "week_end": {"open": 0, "close": 24}
        }
    },
    "FFGR": {
        "id": "3",
        "title": "Fitness Fabrik Griesheim",
        "opening_hours": {
            # MON including FRI
            "week_day": {"open": 8, "close": 23},
            # SAT including SUN
            "week_end": {"open": 8, "close": 21}
        }
    },
}

OPENING_HOURS = STUDIO_MAP.get(LOCATION_SHORT_TITLE)["opening_hours"]
LOCATION_ID = OPENING_HOURS.get("id")
URL = f"https://bodycultureapp.de/ajax/studiocapacity?{LOCATION_ID}"
