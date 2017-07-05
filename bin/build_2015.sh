#!/bin/bash

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q "http://2012-2017.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q "http://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www.assemblee-nationale.fr/qui/Rattachement_partis_2015.pdf" -O pdfs/1412-AN-rattachement-2015.pdf

  wget -q "http://www.assemblee-nationale.fr/14/tribun/xml/liste_rattachement_partis_2015.csv" -O pdfs/1412-AN-rattachement-2015.csv
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/role/declarations_rattachement_parti_politique.pdf" -O pdfs/1412-Sénat-rattachement-2015.pdf
#  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/role/declarations_rattachement_parti_politique_2015.pdf" -O pdfs/1412-Sénat-rattachement-2015.pdf
fi

# Complete CSV AN
bin/complete_an.py pdfs/1412-AN-rattachement-2015.csv > data/1412-AN-rattachement-2015.csv

# PDF Sénat
pdftohtml -xml pdfs/1412-Sénat-rattachement-2015.pdf > /dev/null
bin/convert.py pdfs/1412-Sénat-rattachement-2015.xml 1
bin/convert.py pdfs/1412-Sénat-rattachement-2015.xml > data/1412-Sénat-rattachement-2015.csv

# Build SQLs for ND/NS
bin/build_sql.sh data/1412-AN-rattachement-2015.csv
bin/build_sql.sh data/1412-Sénat-rattachement-2015.csv

