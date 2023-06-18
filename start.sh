#!/bin/bash

# Read additional parameters.
mkdir -p "$PWD/app/data" "$PWD/app/logs" "$PWD/grafana_data"
chmod o+w "$PWD/grafana_data"

# Check if the 'docker-compose' command exists.
if command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null; then
  # ------------------- DEV MODE -------------------
  if [ "$1" == "--dev" ]; then
    # Check if the script is executed with the "--dev --clean" options
    if [ "$2" == "--clean" ]; then 
      # Clean up and remove volumes for development environment
      docker compose -f docker-compose.dev.yml down -v
    # Check if the script is executed with the "--dev --raspi" options
    elif [ "$2" == "--raspi" ]; then 
      # Clean up and remove volumes for Raspberry Pi environment
      docker compose -f docker-compose.raspi.yml down -v
    # Second argument was not provided (or incorrect)
    else
      # Start the services defined in the development Docker Compose file.
      docker compose -f docker-compose.dev.yml up --build
    fi 
  # ------------------- TEST MODE -------------------
  elif [ "$1" == "--test" ]; then
    # Clean up before rebuilding visitor tracker
    rm -rf "$PWD/app/data" "$PWD/app/logs"
    docker compose build visitor-tracker
    # Run only the test script and remove the container afterward
    docker compose -f docker-compose.yml run --rm visitor-tracker sh -c "python3 test_runner.py"
  else
    # DEFAULT: No valid parameters were passed.
    docker compose -f docker-compose.yml up --build
  fi
else
  echo "The command 'docker-compose' does not exist."
fi
