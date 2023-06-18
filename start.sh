#!/bin/bash

# Read additional parameters.

mkdir -p $PWD/app/data $PWD/app/logs  $PWD/grafana_data
chmod o+w $PWD/grafana_data 

# Check if the script is executed with the "--dev --clean" options
if [[ "$1" == "--dev" && "$2" == "--clean" ]]; then
  docker compose -f docker-compose.dev.yml down -v
  rm -rf $PWD/app/data $PWD/app/logs $PWD/postgres
fi

# Check if the 'docker-compose' command exists.
if command -v docker compose >/dev/null 2>&1; then
  if [ "$1" == "--dev" ]; then  # Check if the additional parameter is "--dev".
    docker compose -f ./docker-compose.dev.yml up --build  # Start the services defined in the development Docker Compose file.

  elif [ "$1" == "--test" ]; then
    # 1. do some cleanup
    rm -rf "$PWD/app/data" "$PWD/app/logs"
    # rebuild the visitor tracker 
    docker compose build visitor-tracker

    # run only test script (override restart policy) and then remove the container. 
    docker compose -f docker-compose.yml  run --rm visitor-tracker sh -c "python3 test_runner.py"

  else
    docker compose -f ./docker-compose.yml up --build  # Start the services defined in the Docker Compose file.
  fi
  
  # Check if the script is executed with the "--dev --clean" options
  if [[ "$1" == "--dev" && "$2" == "--clean" ]]; then
    docker compose -f docker-compose.dev.yml down -v
  fi

else
  echo "The command 'docker-compose' does not exist."
fi
