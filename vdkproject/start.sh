#!/bin/sh
python3 manage.py migrate
nohup python3 manage.py run_bot &
python3 manage.py runserver 0.0.0.0:7777 
