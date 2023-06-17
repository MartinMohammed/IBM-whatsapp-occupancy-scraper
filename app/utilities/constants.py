"""Constant values that dont change."""

import os

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