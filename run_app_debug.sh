#!/usr/bin/env bash

# activate virtual environment
. */bin/activate

# run all unit tests
if [[ $1 != "skip" ]]; then
    python3 tester.py
fi

# start app in debug mode
export FLASK_APP=app/feedme_app.py
export FLASK_ENV=development
flask run
