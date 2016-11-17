#!/bin/bash

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

cd "$ROOT_PATH/main"

echo "** Starting Gunicorn..."
gunicorn --config config/gunicorn.py config.wsgi
