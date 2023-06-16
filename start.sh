#!/bin/bash

# Setup the volumes for Grafana:
if [ ! -d "$PWD/grafana_data" ]; then  # Check if the grafana_data directory does not exist
  docker volume create grafana_data    # Create a Docker volume named 'grafana_data'
  docker volume inspect grafana_data   # Inspect the created volume for verification
fi



# The command -v command checks for the existence of the specified command and returns its path if found.
if command -v docker compose >/dev/null 2>&1; then
    docker compose up --build
else
    echo "The command 'docker compose' does not exist."
fi
