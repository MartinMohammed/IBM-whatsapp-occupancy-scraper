#!/bin/bash

# Read additional parameters.
param1="$1"  # The first additional parameter.

# Check if the 'docker' command exists.
if command -v docker >/dev/null 2>&1; then
  # Setup the volumes for Grafana:
  if [ ! -d "$PWD/grafana_data" ]; then  # Check if the 'grafana_data' directory does not exist.
    docker volume create grafana_data    # Create a Docker volume named 'grafana_data'.
    docker volume inspect grafana_data   # Inspect the created volume for verification.
  fi
else
  echo "The command 'docker' does not exist."
fi

# Check if the 'docker-compose' command exists.
if command -v docker compose >/dev/null 2>&1; then
  if [ "$param1" == "--dev" ]; then  # Check if the additional parameter is "--dev".
    docker compose -f ./docker-compose.dev.yml up --build  # Start the services defined in the development Docker Compose file.
  else
    docker compose -f ./docker-compose.yml up --build  # Start the services defined in the Docker Compose file.
  fi
else
  echo "The command 'docker-compose' does not exist."
fi
