#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
ROOT_DIR=$(dirname $SCRIPT_DIR)
python -m unittest discover --pattern='*.py' --start-directory=$ROOT_DIR/src/tests 
