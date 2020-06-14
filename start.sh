#!/bin/bash
app="api"
pip install -r requirements.txt
export FLASK_APP=${app}
flask run