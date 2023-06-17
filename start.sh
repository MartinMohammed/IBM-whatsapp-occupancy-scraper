#!/bin/bash

# Read additional parameters.
param1="$1"  # The first additional parameter.

mkdir -p $PWD/app/data $PWD/app/logs $PWD/portainer_data $PWD/grafana_data
chmod o+w $PWD/grafana_data

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
