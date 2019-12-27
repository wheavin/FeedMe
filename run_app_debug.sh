#!/usr/bin/env bash

# activate virtual environment
. */bin/activate

# run all unit tests
python3 tester.py

# start app in debug mode
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
