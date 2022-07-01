#!/bin/sh
python3 manage.py migrate
nohup python3 manage.py run_bot &
gunicorn vdkproject.wsgi --bind 0.0.0.0:7777
