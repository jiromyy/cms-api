#!/bin/bash

# Update package lists
apt-get update

# Install LibreOffice
sudo apt-get install -y libreoffice

# Start the application
python /home/site/wwwroot/app.py