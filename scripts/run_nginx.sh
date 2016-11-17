#!/bin/bash

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

# Copy Nginx config file.
sudo cp "$PARENT_PATH/nginx.conf" /etc/nginx/

echo "** Starting Nginx..."
sudo service nginx restart
