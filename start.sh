#!/bin/bash

# The command -v command checks for the existence of the specified command and returns its path if found.
if command -v docker compose >/dev/null 2>&1; then
    docker compose up --build
else
    echo "The command 'docker compose' does not exist."
fi
