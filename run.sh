#!/usr/bin/env sh

cd project
gunicorn dietruth.wsgi
