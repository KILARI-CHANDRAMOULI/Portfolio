#!/usr/bin/env bash
# Build script for Render.com — set this as the Build Command.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Load portfolio content from the committed fixture.
python manage.py loaddata fixtures/content.json

# Create the admin user from environment variables.
# Free-tier Render has no shell, so this is the only way in.
# Skips silently if the user already exists.
python manage.py createsuperuser --noinput || true
