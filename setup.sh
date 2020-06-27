#!/bin/sh

echo "===== Installing virtualenv ====="
pip3 install virtualenv --user
sudo apt-get install python3-venv

echo "===== Creating virtualenv ====="
python3 -m venv venv
. venv/bin/activate

echo "===== Installing Requirements ====="
sudo pip3 install -r requirements.txt

echo "===== Creating database ====="
export FLASK_APP=app/feedme_app.py
flask db init
flask db upgrade

echo "===== Creating database schema ====="
python3 setup/create_db_schema.py

echo "===== Creating admin user ====="
python3 setup/create_admin_user.py
