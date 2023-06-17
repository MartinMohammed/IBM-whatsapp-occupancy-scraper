Certainly! Here's an updated README.md file based on the information you provided:

```markdown
# Gym Visitor Tracker

## Overview

The Gym Visitor Tracker is a worker application that monitors gym visitor data by making GET requests to the FitnessFabrik API. It collects data from specific gym locations and stores it for further analysis. This application can be customized to monitor a specific studio by cloning it and configuring the necessary settings.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Error Log Files](#error-log-files)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetches gym visitor data from the FitnessFabrik API
- Stores data in CSV files for further analysis
- Stores data in a PostgreSQL database for easy querying
- Supports customization for different gym locations
- Dockerized for easy deployment

## Requirements

- Docker
- Docker Compose

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd gym-visitor-tracker
   ```

3. Set the required environment variables by creating a `.env` file in the project's root directory. Define the values for the following variables:

   - `REQUEST_DENSITY`: Specifies the frequency of API requests in seconds. Default: 300 seconds (5 minutes).
   - `ENTRIES_UNTIL_FILE_SEGMENTATION`: Defines the number of entries in the CSV file until a new file is created. Default: 1000 entries.
   - `LOCATION_ID`: The ID of the gym location (required).
   - `LOCATION_SHORT_TITLE`: Indicates the location to be tracked based on the gym-mapping.json file (required).
   - `API_URL`: The URL of the FitnessFabrik API (required).
   - `DB_HOSTNAME`: The hostname of the PostgreSQL database (required).
   - `DB_NAME`: The name of the PostgreSQL database (required).
   - `DB_USERNAME`: The username for accessing the PostgreSQL database (required).
   - `DB_PASSWORD`: The password for accessing the PostgreSQL database (required).
   - `DB_PORT`: The port number for the PostgreSQL database (required).

   Make sure to set these environment variables before running the application.

4. Build and start the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start the services defined in the `docker-compose.yml` file.

5. The application will start making GET requests to the FitnessFabrik API, collecting data, and storing it in the `app/data/` directory. The data will also be stored in the PostgreSQL database.

6. Access the PostgreSQL database using a database client or the provided pgAdmin container:

   - **Database Connection Details**:
     - Host: localhost
     - Port: 5432
     - Database: fitness-fabrik-griesheim
     - Username: admin
     - Password: admin123

   - **pgAdmin**:
     - Access pgAdmin in your browser at `http://localhost`.

## Usage

Once the application is running, it will automatically fetch gym visitor data based on the configured settings. The data will be stored in CSV files in the `app/data/` directory and in the PostgreSQL database. You can access and analyze the data using the provided files and database connection.

The application will continue running and fetching data at the specified frequency until it is manually stopped.

## Configuration

The Gym Visitor Tracker application

 provides configurable settings through environment variables. These variables are set in the `.env` file. Here are the available settings:

- `REQUEST_DENSITY`: Specifies the frequency of API requests in seconds. Default: 300 seconds (5 minutes).
- `ENTRIES_UNTIL_FILE_SEGMENTATION`: Defines the number of entries in the CSV file until a new file is created. Default: 1000 entries.
- `LOCATION_ID`: The ID of the gym location (required).
- `LOCATION_SHORT_TITLE`: Indicates the location to be tracked based on the gym-mapping.json file (required).
- `API_URL`: The URL of the FitnessFabrik API (required).
- `DB_HOSTNAME`: The hostname of the PostgreSQL database (required).
- `DB_NAME`: The name of the PostgreSQL database (required).
- `DB_USERNAME`: The username for accessing the PostgreSQL database (required).
- `DB_PASSWORD`: The password for accessing the PostgreSQL database (required).
- `DB_PORT`: The port number for the PostgreSQL database (required).

Make sure to set these environment variables correctly before running the application.

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

## Error Log Files

The application generates the following error log files:

- `error.log`: Logs errors that occur during application startup or missing user configurations.
- `requests.log`: Logs errors related to HTTP requests, such as fetching data from the API or writing data.
- `db.log`: Records events related to database operations, including querying data from the database or creating new data.

These log files can be used for troubleshooting and resolving issues.

## Contributing

Contributions to the Gym Visitor Tracker project are welcome! If you find any issues or want to suggest improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

Please note that you may need to update the repository URL and adjust any other information or sections as needed for your specific project.