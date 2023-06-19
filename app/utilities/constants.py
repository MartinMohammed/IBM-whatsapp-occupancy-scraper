import os
import sys
from . import utils_log


# Constant values such as settings inferred from environment.

# Path to the root directory ("/app" inside the Docker container).
PATH_TO_ROOT = os.getcwd()


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
    LOCATION_SHORT_TITLE = os.getenv("LOCATION_SHORT_TITLE").lower()  # Indicates the location to be tracked based on the gym-mapping.json file.
    assert LOCATION_SHORT_TITLE is not None, "LOCATION_SHORT_TITLE was not provided."

    # Create the data directory if it doesn't exist.
    LOCATION_DATA_DIR = os.path.join(PATH_TO_ROOT, LOCATION_SHORT_TITLE, "data",)
    if not os.path.exists(LOCATION_DATA_DIR):
        os.makedirs(LOCATION_DATA_DIR, exist_ok=True)

    # Create the log directory if it doesn't exist.
    LOCATION_LOG_DIR = os.path.join(PATH_TO_ROOT, LOCATION_SHORT_TITLE, "logs")
    if not os.path.exists(LOCATION_LOG_DIR):
        os.makedirs(LOCATION_LOG_DIR, exist_ok=True)

except AssertionError as e:
    error_file_path = os.path.join(LOCATION_LOG_DIR, "logs.error")
    utils_log.log(f"Location Short Title: {LOCATION_SHORT_TITLE} --> {e}", error_file_path)
    sys.exit(1)

# ----------------------- SETTINGS -----------------------


# Studios are identified by their LOCATION SHORT NAME:
STUDIO_MAP = {
    "ffda": {
        "id": "1",
        "title": "Fitness Fabrik Darmstadt",
        "opening_hours": {
            # MON including FRI
            "week_day": {"open": 8, "close": 23},
            # SAT including SUN
            "week_end": {"open": 10, "close": 21}
        }
    },
    "ffhb": {
        "id": "2",
        "title": "Fitness Fabrik Darmstadt (Hbf)",
        "opening_hours": {
            # MON including FRI
            "week_day": {"open": 0, "close": 24},
            # SAT including SUN
            "week_end": {"open": 0, "close": 24}
        }
    },
    "ffgr": {
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

STUDIO = STUDIO_MAP.get(LOCATION_SHORT_TITLE)
OPENING_HOURS = STUDIO["opening_hours"]
STUDIO_ID = int(STUDIO.get("id"))
URL = f"https://bodycultureapp.de/ajax/studiocapacity?apiToken=5"
