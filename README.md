# Fitness App Suite

Welcome to the Fitness App Suite, a collection of applications developed during my internship at IBM in collaboration with the Body Culture Group in Darmstadt. This suite includes the Gym Occupancy Tracker, a Svelte Frontend Dashboard, a Webhook API Server, an Authorization Server with JWT, and the successful WhatsApp Middleware npm package.

## Overview

During my internship at IBM, I took on the role of Product Owner for a project in collaboration with the Body Culture Group in Darmstadt. Body Culture is a prominent player in the fitness industry with over 300 employees in Hessen and multiple sub-brands, dominating the market in the Rhine-Main Area.

As part of my responsibilities, I led the design of a comprehensive AWS Cloud Infrastructure. This involved various tasks such as networking with VPCs and implementing essential services like API Gateway and DynamoDB. To achieve rapid and efficient cloud infrastructure deployment and updates, I utilized the Cloud Development Kit as an Infrastructure as Code technology.

The primary focus of the project was to integrate a custom WhatsApp Chatbot using the Meta WhatsApp Cloud API. To accomplish this, I developed a fully functional WhatsApp Dashboard using Svelte, a high-speed JavaScript Framework. For the backend, I employed REST API and WebSockets for real-time message communication. Security was a crucial aspect, and I ensured robust protection by implementing JWT authentication and leveraging AWS Cognito service to safeguard the API Gateway.

The success of the WhatsApp Chatbot was impressive, as it garnered widespread interest and achieved over 4000 weekly downloads on NPM within the first two weeks of its release. Additionally, I integrated the WhatsAppBot with Google's Dialogflow, allowing the bot to utilize artificial intelligence to respond to user messages in the fitness studios. This innovative approach effectively transformed customer service from traditional telephone communication to fully automated interactions via WhatsAppBot, resulting in increased conversion rates for new customer sign-ups. Users could easily share the WhatsApp business account with friends, while the bot handled all membership-related information, including scheduling a suitable slot within a week.

### Quick navigation 

- [Svelte Frontend Dashboard Repository](https://github.com/MartinMohammed/IBM-whatsapp-bot-frontend)
- [WhatsApp Backend Server Repository](https://github.com/MartinMohammed/IBM-whatsapp-bot-backend)
- [Authorization Server Repository](https://github.com/MartinMohammed/IBM-jwt-authorization)
- [WhatsApp Middleware NPM Package](https://github.com/MartinMohammed/IBM-whatsapp-bot-middleware-npm)


## Svelte Frontend Dashboard

The Svelte Frontend Dashboard is a web application designed for the CRS team to interact with gym members and facilitate automated WhatsApp customer service. Built with Svelte, it utilizes websockets to fetch real-time data from the backend, including recent WhatsApp messages. The production version includes a permission system, enabling admin privileges and integration with Google's Dialogflow chatbot AI.

![Login Screen](https://github.com/MartinMohammed/whataspp-dashboard-svelte/assets/81469658/9cc033d6-48c3-4efd-bd2d-b81fce6df6c3.png)

![Chat Screen](https://github.com/MartinMohammed/whataspp-dashboard-svelte/assets/81469658/377f62d9-581f-4230-b6c0-e3f20f5a4c23.png)
## WhatsApp Backend Server

The WhatsApp Backend server is responsible for delivering new incoming messages to the WhatsApp dashboard and thus to the customer service in real time using web sockets and sending messages to gym members via the WhatsApp Cloud API. It provides a protected REST API and as well a web socket server. It stores all messages that were sent in a NoSQL database on AWS.

[Link to WhatsApp Backend Server Repository](https://github.com/MartinMohammed/IBM-whatsapp-bot-backend)

## Authorization Server with JWT

The Authorization Server with JWT is a secure authentication service that allows users to register, login, and manage their authentication tokens. It provides endpoints for user registration, user login, refreshing access tokens, and logging out. The API uses JWTs for authentication and Redis for managing refresh tokens.

[Link to Authorization Server Repository](https://github.com/MartinMohammed/IBM-jwt-authorization)


# Gym Occupancy Tracker

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
   git clone https://github.com/MartinMohammed/IBM-whatsapp-occupancy-scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd gym-visitor-tracker
   ```

3. Set the required environment variables by creating a `.env` file in the project's root directory. Define the values for the following variables:

   - `REQUEST_DENSITY`: Specifies the frequency of API requests in seconds. Default: 300 seconds (5 minutes).
   - `ENTRIES_UNTIL_FILE_SEGMENTATION`: Defines the number of entries in the CSV file until a new file is created. Default: 1000 entries.
   - `STUDIO_ID`: The ID of the gym location (required).
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
- `STUDIO_ID`: The ID of the gym location (required).
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

## WhatsApp Middleware NPM Package

The WhatsApp Middleware Package is a highly successful npm package developed during my internship at IBM. It serves as a crucial component of the Fitness App Suite, enabling seamless integration with the WhatsApp Chatbot and real-time message communication.

[Link to WhatsApp Middleware NPM package](https://github.com/MartinMohammed/IBM-whatsapp-bot-middleware-npm)


## Conclusion

The Fitness App Suite brings together a range of applications to improve the fitness experience for users and streamline customer service. Each application serves a specific purpose in the overall ecosystem, offering features such as gym occupancy tracking, real-time notifications, and secure authentication.

Feel free to explore each application's repository for more details and contributions. If you have any questions or suggestions, don't hesitate to reach out. Happy coding!
