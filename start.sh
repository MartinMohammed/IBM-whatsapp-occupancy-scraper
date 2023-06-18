#!/bin/bash

# Read additional parameters.
mkdir -p "$PWD/app/data" "$PWD/app/logs" "$PWD/grafana_data"
chmod o+w "$PWD/grafana_data"


# Check if the 'docker-compose' command exists.
if command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null; then

  # Check if the script is executed with the "--dev --clean" options
  if [[ "$1" == "--dev" && "$2" == "--clean" ]]; then
    # Clean up and remove volumes for development environment
    docker compose -f docker-compose.dev.yml down -v
    exit 0 
  fi

  # Check if the script is executed with the "--dev --raspi" options
  if [[ "$1" == "--dev" && "$2" == "--raspi" ]]; then
    # Clean up and remove volumes for Raspberry Pi environment
    docker compose -f docker-compose.raspi.yml down -v
    exit 0 
  fi

  if [ "$1" == "--dev" ]; then
    # Start the services defined in the development Docker Compose file.
    docker compose -f docker-compose.dev.yml up --build
    exit 0
  elif [ "$1" == "--test" ]; then
    # Clean up before rebuilding visitor tracker
    rm -rf "$PWD/app/data" "$PWD/app/logs"
    docker compose build visitor-tracker
    # Run only the test script and remove the container afterward
    docker compose -f docker-compose.yml run --rm visitor-tracker sh -c "python3 test_runner.py"
    exit 0
  else
    # Start the services defined in the Docker Compose file.
    docker compose -f docker-compose.yml up --build
    exit 0
  fi


else
  echo "The command 'docker-compose' does not exist."
fi
