#!/bin/sh

export PATH="$PATH:/code/.pip-cache/bin"

echo "===== Creating virtualenv ====="
. venv/bin/activate

echo "===== Installing Requirements ====="
pip install --user pipenv
pip install -r requirements.txt

echo "===== Creating database ====="
export FLASK_APP=app/feedme_app.py
echo "Flask app set to: $FLASK_APP"
flask db init
flask db upgrade

echo "===== Creating database schema ====="
python create_db_schema.py

echo "===== Creating admin user ====="
python create_admin_user.py
