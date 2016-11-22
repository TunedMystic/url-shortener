#!/bin/bash

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )


# Create directories for the environment.
sudo mkdir -p "$ROOT_PATH/logs"
sudo mkdir -p "$ROOT_PATH/static"
sudo mkdir -p "$ROOT_PATH/ssl"
sudo mkdir -p /app


# Create symbolic links.
sudo ln -s "$ROOT_PATH/logs/" /app/logs
sudo ln -s "$ROOT_PATH/static/" /app/static
sudo ln -s "$ROOT_PATH/ssl/" /app/ssl
