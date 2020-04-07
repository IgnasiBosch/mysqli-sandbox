#!/bin/sh

cd /app
pip3 install -r /app/requirements.txt
flask run  --host=0.0.0.0