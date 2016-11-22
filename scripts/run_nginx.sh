#!/bin/bash

# Nginx config filename.
NGINX_CONF="nginx.conf"

# Site config.
SITE_NAME="server.dev"
SITE_CONF="$SITE_NAME.conf"

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )

# Copy Nginx config file.
sudo cp "$PARENT_PATH/$NGINX_CONF" /etc/nginx/

# Remove content from sites-enabled and sites-available.
sudo rm /etc/nginx/sites-available/*
sudo rm /etc/nginx/sites-enabled/*

# Copy site config and create symlink.
sudo cp "$PARENT_PATH/$SITE_CONF" "/etc/nginx/sites-available/$SITE_CONF"
sudo ln -s "/etc/nginx/sites-available/$SITE_CONF" "/etc/nginx/sites-enabled/$SITE_NAME"

echo "** Starting Nginx..."
sudo service nginx restart
