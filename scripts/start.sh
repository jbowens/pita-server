#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
ROOT=$SCRIPT_DIR/..
python $ROOT/src/server.py
