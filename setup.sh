#!/bin/sh

echo "Installing virtualenv"
pip3 install virtualenv --user
sudo apt-get install python3-venv

echo "Creating virtualenv"
python3 -m venv venv
. venv/bin/activate

echo "Installing Requirements"
sudo pip3 install -r requirements.txt

echo "Creating database"
flask db upgrade
