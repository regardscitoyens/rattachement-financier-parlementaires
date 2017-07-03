#!/bin/bash

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q "http://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q "https://www.interieur.gouv.fr/content/download/103183/814645/file/liste-candidats-partis-politiques.pdf" -O pdfs/1706-Beauvau-rattachement-candidats-LG2017.pdf
  wget -q "https://raw.githubusercontent.com/alphoenix/donnees/master/rattachement_LG2017.csv" -O data/1706-Beauvau-rattachement-candidats-LG2017.csv
fi

# Filter elected 
bin/filter_an.py data/1706-Beauvau-rattachement-candidats-LG2017.csv > data/1706-AN-rattachement-2017.csv

# Build SQL for ND
bin/build_sql.sh data/1706-AN-rattachement-2017.csv

