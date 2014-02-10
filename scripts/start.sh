#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
ROOT=$SCRIPT_DIR/..
$SCRIPT_DIR/reconstruct-db.sh
python $ROOT/src/server.py
