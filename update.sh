#!/bin/bash

cd $(dirname $0)
. venv/bin/activate

git reset --hard HEAD
git pull https://github.com/XUJINKAI/DuoBlog.git
chmod +x update.sh

cd site
pip3 install -r requirements.txt
python manage.py migrate
echo yes | python manage.py collectstatic
