#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
SQL_DIR=$SCRIPT_DIR/../sql
cat "$SQL_DIR/drop-everything.sql" \
    "$SQL_DIR/accounts.sql" \
    "$SQL_DIR/pitas.sql" \
    | psql --dbname=mylittlepita --file=-
