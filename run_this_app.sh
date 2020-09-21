#!/bin/bash
. venv/bin/activate
export FLASK_APP=app
flask init-db
flask run
