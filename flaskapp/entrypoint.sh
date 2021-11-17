#!/bin/sh

gunicorn --reload -w 1 --bind 0.0.0.0:5000 wsgi
