#!/bin/sh

cd /var/www/whatsmyworkout
git pull https://github.com/heidricklevi/whatsmyworkout.git
cd whatsmyworkout-vue
npm run build
yes | sudo \cp -rf dist ../account/static/
cd ..
yes | python3 manage.py collectstatic