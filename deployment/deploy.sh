#!/bin/sh

cd /var/www/whatsmyworkout
git pull
pip install -r requirements.txt
sudo uwsgi --ini whatsmyworkout/whatsMyWorkoutServices.ini
service nginx restart