#!/bin/bash
apt-get update
apt-get install -y libreoffice
gunicorn --bind=0.0.0.0 --timeout 600 app:app