#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
ROOT=$SCRIPT_DIR/..
if [ -f $ROOT/config/personal.cfg ]; then
    export MLP_API_CONFIG_FILE="../../config/personal.cfg"
fi
python $ROOT/src/server.py
