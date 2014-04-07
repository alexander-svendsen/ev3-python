#!/bin/bash
# Shellscript for running the server for linux users

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
        exit 0
}

BASEDIR=..
export PYTHONPATH=$PYTHONPATH:$BASEDIR
cd server # Must be inside this directory to get static to work

#change the python file arguments if you wish to change some configuration
python server.py
