#!/bin/bash

# Update package lists
apt-get update

# Install LibreOffice
apt-get install -y libreoffice

# Start your main application
python /home/site/wwwroot/app.py