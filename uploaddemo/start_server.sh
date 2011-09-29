#!/bin/bash

PATH=/sbin:/bin:/usr/sbin:/usr/bin
export DJANGO_SETTINGS_MODULE=uploaddemo.settings
PORT=8080
umask 027

FASTCGI_OPTS="minspare=1 maxspare=1 maxchildren=4 maxrequests=10000"

echo "Starting FastCGI server for upload demo"
python manage.py runfcgi daemonize=false umask=027 host=localhost port=${PORT} ${FASTCGI_OPTS}
