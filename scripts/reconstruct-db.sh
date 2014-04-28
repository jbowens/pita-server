#!/usr/bin/env bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
SQL_DIR=$SCRIPT_DIR/../sql
cat "$SQL_DIR/drop-everything.sql" \
    $SQL_DIR/schema.sql \
    | psql --dbname=mylittlepita --file=- --user=pita
# Load the dictionary words into the database
python scripts/dictionary.py load
