#!/bin/bash

# Update package lists
sudo apt-get update

# Install LibreOffice
sudo apt-get install -y libreoffice

# Start the application
python /home/site/wwwroot/app.py >> /home/site/startup.log 2>&1