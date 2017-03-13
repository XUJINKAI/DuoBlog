#!/bin/bash

cd $(dirname $0)
. venv/bin/activate
git pull http://repo.xujinkai.net/x/code-tango.git
cd site
python manage.py migrate
echo yes | python manage.py collectstatic
