#!/bin/bash

sudo apt-get update

sudo apt-get -y upgrade

sudo apt-get install -y python3-dev
sudo apt-get install -y python3-pip
sudo apt-get install -y nginx
sudo apt-get install -y sqlite3
sudo apt-get install -y tree
sudo apt-get install -y screen

sleep 3

# Set up database user and 
# bash /home/vagrant/devbox/bootstrap-db.sh

# Create logs directory for django (this depends on the environment).
# sudo mkdir /vagrant/logs/
