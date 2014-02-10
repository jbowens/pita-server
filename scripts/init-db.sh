#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
SQL_DIR=$SCRIPT_DIR/../sql
psql --file=$SQL_DIR/default-db-init.sql
