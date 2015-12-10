#!/bin/bash

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q "http://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q "http://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www.assemblee-nationale.fr/qui/Rattachement_partis_2016.pdf" -O pdfs/1512-AN-rattachement-2016.pdf
  echo "Nom;Prénom;Groupe;Parti ou groupement politique" | iconv -t ISO88591 > pdfs/1512-AN-rattachement-2016.csv
  wget -q "http://www.assemblee-nationale.fr/14/tribun/xml/liste_rattachement_partis_2016.csv" -O - | sed 's/\r//' >> pdfs/1512-AN-rattachement-2016.csv
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/role/declarations_rattachement_parti_politique_2016.pdf" -O pdfs/1512-Sénat-rattachement-2016.pdf
fi

# Complete CSV AN
bin/complete_an.py pdfs/1512-AN-rattachement-2016.csv > data/1512-AN-rattachement-2016.csv

# PDF Sénat
pdftohtml -xml pdfs/1512-Sénat-rattachement-2016.pdf > /dev/null
bin/convert.py pdfs/1512-Sénat-rattachement-2016.xml 1
bin/convert.py pdfs/1512-Sénat-rattachement-2016.xml > data/1512-Sénat-rattachement-2016.csv

# Build SQLs for ND/NS
bin/build_sql.sh data/1512-AN-rattachement-2016.csv
bin/build_sql.sh data/1512-Sénat-rattachement-2016.csv

