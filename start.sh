#!/bin/bash

# Create directories for individual studios and services defined in Docker Compose
create_directories() {
  local directories=(
    "$PWD/app/data/ffgr/data" "$PWD/app/logs/ffgr/logs"
    "$PWD/app/data/ffda/data" "$PWD/app/logs/ffda/logs"
    "$PWD/app/data/ffhb/data" "$PWD/app/logs/ffhb/logs"
    "$PWD/grafana_data"  "$PWD/postgres"
  )
  # Create every directory in the list inside the container.
  for dir in "${directories[@]}"; do
    mkdir -p "$dir"
  done

  chmod o+w "$PWD/grafana_data" "$PWD/postgres"
}

# Clean up and remove volumes for development environment
clean_dev_environment() {
  docker compose -f docker-compose.dev.yml down -v
  local directories=(
    "$PWD/app/data/ffgr" "$PWD/app/logs/ffgr"
    "$PWD/app/data/ffda" "$PWD/app/logs/ffda"
    "$PWD/app/data/ffhb" "$PWD/app/logs/ffhb"
    "$PWD/grafana_data/" "$PWD/postgres/"
  )

  for dir in "${directories[@]}"; do
    rm -rf "$dir"
  done
}

# Start the services defined in the development Docker Compose file
start_dev_services() {
  create_directories  # Call create_directories to have the required folders created. 
  docker compose -f docker-compose.dev.yml up --build
}

# Start the services defined in the development Docker Compose file for Raspberry Pi
start_raspi_services() {
  create_directories  # Call create_directories to have the required folders created. 
  docker compose -f docker-compose.raspi.yml up --build
}

# Start the services defined in the production Docker Compose file
start_production_services() {
  create_directories  # Call create_directories to have the required folders created. 
  docker compose -f docker-compose.yml up --build
}

# Clean up before rebuilding visitor tracker and run tests
run_tests() {
  clean_dev_environment  # Call clean_dev_environment to have a fresh setup

  local services=("ffgr" "ffda" "ffhb")

  for service in "${services[@]}"; do
    docker compose build "$service"
    docker compose -f docker-compose.yml run --rm "$service" sh -c "python3 test_runner.py"
  done
}

# Check if the 'docker-compose' command exists
if command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null; then
  case $1 in
    "--dev")
      case $2 in
        "--raspi") start_raspi_services ;;
        *) start_dev_services ;;
      esac
      ;;
    "--clean")
      clean_dev_environment ;;
    "--test")
      run_tests ;;
    *)
      start_production_services ;;
  esac
else
  echo "The command 'docker-compose' does not exist."
fi
