#!/bin/bash

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )
ETC_PATH="$ROOT_PATH/etc"

# Create directories for the environment.
sudo mkdir -p "$ETC_PATH/log"
sudo mkdir -p "$ETC_PATH/ssl"
sudo mkdir -p "$ETC_PATH/static"
sudo mkdir -p /app

# Clear existing symlinks
sudo rm -rf /app/*

# Create symbolic links.
sudo ln -s "$ETC_PATH/log/" /app/log
sudo ln -s "$ETC_PATH/ssl/" /app/ssl
sudo ln -s "$ETC_PATH/static/" /app/static
