#!/usr/bin/env bash

cd /var/www/whatsmyworkout
git pull https://github.com/heidricklevi/whatsmyworkout.git
cd whatsmyworkout-vue
npm run build
cp dist ../account/static/
cd ..
python3 manage.py collectstatic