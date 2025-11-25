#!/bin/bash
echo "Running Django migrations..."

# Crée les migrations locales si nécessaire
python3 manage.py makemigrations

# Applique toutes les migrations sur la base Render
python3 manage.py migrate --noinput

echo "Migrations applied successfully!"
