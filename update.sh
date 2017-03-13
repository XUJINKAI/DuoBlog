#!/bin/bash

cd $(dirname $0)
. venv/bin/activate

while true; do
	read -p "RESET git repo (clean) and pull remote repo ? (Y/N)" yn
	case $yn in
		[Yy]* )
			git reset --hard HEAD
			git pull http://repo.xujinkai.net/x/code-tango.git
			break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	esac
done

cd site
pip3 install -r requirements.txt
python manage.py migrate
echo yes | python manage.py collectstatic
