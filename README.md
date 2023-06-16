# Project Documentation

## Overview
This project serves as a worker application for making GET requests to the FitnessFabrik API and collecting data from specific gym locations. The main objective is to monitor the number of visitors in each studio and store the data for further analysis. The application can be cloned and dedicated to monitoring a specific studio.


## Settings
The application utilizes several settings that can be configured to customize its behavior. These settings are stored in environment variables and should be properly set before running the application. Here are the available settings:

* `REQUEST_DENSITY`: Specifies the frequency of API requests in seconds. The default value is 300 seconds (5 minutes).
* `ENTRIES_UNTIL_FILE_SEGMENTATION`: Defines the number of entries in the CSV file until a new file is created. The default value is 1000 entries.
* `LOCATION_ID`: The ID of the gym location. This value must be provided.
* `LOCATION_SHORT_TITLE`: Indicates the location to be tracked based on the gym-mapping.json file. This value must be provided.
* `API_URL`: The URL of the FitnessFabrik API. This value must be provided.

Please make sure to set these environment variables before running the application.

## File Structure
The project has the following file structure:

```
- app/
    - data/                  # Directory for storing data files
    - logs/                  # Directory for storing log files
    - utilities/             # Directory containing utility functions
        - __init__.py
        - constants.py       # File containing constant values
        - utils.py           # File containing utility functions
    - main.py                # Main script for running the worker
    - Dockerfile             # Dockerfile for building the application container
    - docker-compose.yml     # Docker Compose file for container configuration
- tests/
    - test_main.py           # Unit tests for the main script
- .env                     # Environment file for setting environment variables
- requirements.txt         # List of Python dependencies
- README.md                # Documentation file (you are reading it)
```

## Error Files

### error.log
The `error.log` file is used for logging errors that occur during the startup of the application or missing user configurations. The following situations are logged to this file:

* Missing configuration of the user for starting the worker (e.g., not setting the required environment variables).
* General errors that occurred during the startup of the application.

### requests.log
The `requests.log` file is used for logging errors that occur during HTTP requests, such as fetching data from the API or writing data. Any errors related to HTTP requests are logged to this file.

### db.log
The `db.log` file is utilized to record database events that occur during database requests, including querying data from the database or creating new data. This file serves as a log for any errors or events associated with the database operations.

Please refer to these error log files for troubleshooting and resolving issues related to the application.

## Usage
To run the application, follow these steps:

1. Set the required environment variables by creating a `.env` file in the project's root directory and defining the values for `REQUEST_DENSITY`, `ENTRIES_UNTIL_FILE_SEGMENTATION`, `LOCATION_ID`, `LOCATION_SHORT_TITLE`, and `API_URL`.
2. Build and run the application using Docker Compose. Ensure that Docker Compose is installed on your system. Run the following command in the project's root directory:

```
docker-compose up --build
```

3. The application will start making GET requests to the FitnessFabrik API, collecting data, and storing it in the `data/` directory.

## Conclusion
This documentation provides an overview of the project, its settings, file structure, and information about the error log files. Follow the provided instructions to set up and run the application successfully. If you encounter any issues, refer to the error log files for troubleshooting.