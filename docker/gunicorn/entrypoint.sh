#!/usr/bin/env sh
set -e

if [ -f /app/engine/runserver.py ]; then
    DEFAULT_MODULE_NAME=engine.runserver
elif [ -f /app/runserver.py ]; then
    DEFAULT_MODULE_NAME=runserver
fi

echo $DEFAULT_MODULE_NAME
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi

export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
echo $MODULE_NAME
echo $APP_MODULE
echo $GUNICORN_CONF
echo $VARIABLE_NAME

exec "$@"