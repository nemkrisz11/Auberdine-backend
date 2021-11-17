#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/var/www/flaskapp:/var/www
python -m pytest -v /var/www/test
