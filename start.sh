#!/bin/bash

# Update package lists
apt-get update

# Install LibreOffice
apt-get install -y libreoffice

# Start your main application
gunicorn --bind=0.0.0.0 --timeout 600 app:app
