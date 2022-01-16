#!/usr/bin/env bash

export PATH="$PATH:/code/.pip-cache/bin"

# activate virtual environment
. */bin/activate

# run all unit tests
if [[ $1 == "skip" ]]; then
    echo "Skipping tests"
else
    python3 tester.py
fi

# start app in debug mode
export FLASK_APP=app/feedme_app.py
export FLASK_ENV=development
flask run
