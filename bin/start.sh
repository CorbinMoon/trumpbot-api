#!/bin/bash
app="api.py"
export FLASK_APP=${app}
python -m flask run --host=0.0.0.0