# Project Documentation

## Overview
This project serves as a worker application for monitoring gym visitor data by making GET requests to the FitnessFabrik API. It collects data from specific gym locations and stores it for further analysis. You can clone the application and customize it to monitor a specific studio.

## Settings
The application offers configurable settings stored in environment variables. Before running the application, ensure these variables are properly set. Here are the available settings:

- `REQUEST_DENSITY`: Specifies the frequency of API requests in seconds. Default: 300 seconds (5 minutes).
- `ENTRIES_UNTIL_FILE_SEGMENTATION`: Defines the number of entries in the CSV file until a new file is created. Default: 1000 entries.
- `LOCATION_ID`: The ID of the gym location (required).
- `LOCATION_SHORT_TITLE`: Indicates the location to be tracked based on the gym-mapping.json file (required).
- `API_URL`: The URL of the FitnessFabrik API (required).

Make sure to set these environment variables before running the application.

## File Structure
The project follows the following file structure:

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
The `error.log` file logs errors that occur during application startup or missing user configurations. It captures situations such as missing required environment variables or general startup errors.

### requests.log
The `requests.log` file logs errors related to HTTP requests, such as fetching data from the API or writing data. Any errors associated with HTTP requests are recorded here.

### db.log
The `db.log` file records events related to database operations, including querying data from the database or creating new data. It serves as a log for any errors or events related to the database.

Please refer to these error log files for troubleshooting and resolving issues.

## Usage
To run the application, follow these steps:

1. Set the required environment variables by creating a `.env` file in the project's root directory. Define the values for `REQUEST_DENSITY`, `ENTRIES_UNTIL_FILE_SEGMENTATION`, `LOCATION_ID`, `LOCATION_SHORT_TITLE`, and `API_URL`.
2. Build and run the application using Docker Compose. Make sure you have Docker Compose installed. Run the following command in the project's root directory:

```
docker-compose up --build
```

3. The application will start making GET requests to the FitnessFabrik API, collecting data, and storing it in the `data/` directory.

4. Access the PostgreSQL database using a database client or the provided pgAdmin container:

- **Database Connection Details**:
  - Host: localhost
  - Port: 5432
  - Database: fitness-fabrik-griesheim
  - Username: admin
  - Password: admin123

- **pgAdmin**:
  - Access pgAdmin in your browser at `http://localhost`.

## Conclusion
This documentation provides an overview of the project, its settings, file structure, and information about the error

 log files. Follow the provided instructions to set up and run the application successfully. If you encounter any issues, refer to the error log files for troubleshooting.

## Contributing

Contributions to the Visitor Tracker project are welcome! If you find any issues or want to suggest improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).