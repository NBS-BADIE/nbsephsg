#!/bin/bash
# Script pour appliquer les migrations sur Render
echo "Running Django migrations..."
python manage.py migrate --noinput
echo "Migrations applied successfully!"
