#!/bin/bash
#Bash Script to act as an entrypoint to help us decide if we want to debug the app or run the app

SCRIPT_NAME=$(basename "$0")

function production_run() {
    gunicorn -c $APP_CONFIG $APP_MODULE
}


function simple_format_msg_echo() {
   echo "$(date) ${SCRIPT_NAME} ${1}"
}


simple_format_msg_echo "Starting Entrypoint Script"
production_run
