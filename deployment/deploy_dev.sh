#!/bin/sh

cd /var/www/whatsmyworkout
git reset
sudo git pull https://github.com/heidricklevi/whatsmyworkout.git
cd whatsmyworkout-vue
npm run build
yes | sudo cp -rf dist ../account/static/
cd ..
python3 manage.py collectstatic --noinput
