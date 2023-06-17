#!/bin/bash

# Read additional parameters.
param1="$1"  # The first additional parameter.

mkdir -p $PWD/app/data $PWD/app/logs  $PWD/grafana_data
chmod o+w $PWD/grafana_data 

# Check if the script is executed with the "--dev --clean" options
if [[ "$1" == "--dev" && "$2" == "--clean" ]]; then
  docker compose -f docker-compose.dev.yml down -v
  rm -rf $PWD/app/data $PWD/app/logs $PWD/postgres
fi

# Check if the 'docker-compose' command exists.
if command -v docker compose >/dev/null 2>&1; then
  if [ "$param1" == "--dev" ]; then  # Check if the additional parameter is "--dev".
    docker compose -f ./docker-compose.dev.yml up --build  # Start the services defined in the development Docker Compose file.
  else
    docker compose -f ./docker-compose.yml up --build  # Start the services defined in the Docker Compose file.
  fi

  # Check if the script is executed with the "--dev --clean" options
  if [[ "$1" == "--dev" && "$2" == "--clean" ]]; then
    docker-compose -f docker-compose.dev.yml down -v
  fi

else
  echo "The command 'docker-compose' does not exist."
fi
