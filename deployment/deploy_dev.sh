#!/bin/sh

cd /var/www/whatsmyworkout
git pull https://github.com/heidricklevi/whatsmyworkout.git
cd whatsmyworkout-vue
npm run build
yes | \cp -rf dist ../account/static/
cd ..
python3 manage.py collectstatic --noinput
service apache2 restart