#!/bin/bash

CACHE=$1
mkdir -p pdfs pdfmaps cache data

if [ -z "$CACHE" ]; then
  wget -q "http://2012-2017.nosdeputes.fr/deputes/json" -O cache/deputes.json
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

# ./bin/convert.sh 1 ; cat data/* | awk -F '","' '{print $4}' | count
#echo "## Rattachement financier des députés à un parti politique pour 2014" > README.md
#echo >> README.md
#
#echo "### Répartition des 577 députés par parti de rattachement :<br/>" >> README.md
#cat rattachement-deputes-2014.csv |
# grep -v ',"rattachement_parti'   |
# awk -F '","' '{print $4}'        |
# sed 's/"$//'                     |
# sort | uniq -c >> README.md
#echo >> README.md
#
#echo "### Répartition des députés des différents groupe politique par parti de rattachement :<br/>" >> README.md
#cat rattachement-deputes-2014.csv |
# grep -v ',"rattachement_parti'   |
# awk -F '","' '{print $3" - "$4}' |
# sed 's/"$//'                     |
# sort | uniq -c >> README.md
#echo >> README.md
#
