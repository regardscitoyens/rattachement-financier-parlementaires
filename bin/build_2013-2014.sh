#!/bin/bash

CACHE=$1
mkdir -p pdfs pdfmaps cache data

if [ -z "$CACHE" ]; then
  wget -q "http://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q "http://www.assemblee-nationale.fr/qui/Rattachement_partis.pdf" -O pdfs/1212-AN-rattachement-2013.pdf
  wget -q "http://www.assemblee-nationale.fr/qui/Rattachement_partis_2014.pdf" -O pdfs/1312-AN-rattachement-2014.pdf
  wget -q "http://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/role/Liste_rattachements_site_internet_2013.pdf" -O pdfs/1212-Sénat-rattachement-2013.pdf
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/role/declarations_rattachement_parti_politique.pdf" -O pdfs/1312-Sénat-rattachement-2014.pdf
fi

for pdffile in pdfs/*.pdf; do
  pdftohtml -xml "$pdffile" > /dev/null
  xmlfile=$(echo $pdffile | sed 's/\.pdf$/.xml/')
  # draw maps
  ./bin/convert.py "$xmlfile" 1
  csvfile=$(echo $pdffile | sed 's/\.pdf$/.csv/' | sed 's#pdfs/#data/#')
  ./bin/convert.py "$xmlfile" > "$csvfile"
done
