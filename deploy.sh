#!/bin/bash
set -x
set -e

python="/srv/venv/paperlibrary/bin/python"

manage="sudo -u paperlibrary $python manage.py"

git pull

#$manage scss
$manage collectstatic --noinput
$manage migrate

sudo systemctl reload paperlibrary.service
