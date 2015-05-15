#!/bin/bash

mkdir -p sql

in=$1
out=$(echo $1 | sed 's|data/|sql/|' | sed 's|\.csv|.sql|')

cat $in | grep -v '^"nom","' | while read line; do
  parti=$(echo $line | awk -F '","' '{print $4}')
  slug=$(echo $line | awk -F '","' '{print $7}')
  echo "UPDATE parlementaire SET parti = \"$parti\" WHERE parlementaire.slug = '$slug';"
done > $out
