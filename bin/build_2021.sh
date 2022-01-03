#!/bin/bash

# AN https://www2.assemblee-nationale.fr/static/15/rattachement_partis/liste_rattachement_partis_2021.csv

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q --no-check-certificate "https://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q --no-check-certificate "https://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www2.assemblee-nationale.fr/deputes/liste/partis-politiques/(annee)/2021" -O pdfs/2101-AN-rattachement-2021.html
  echo "Nom_de_famille;ID_AN;Nom;Groupe;Parti ou groupement politique"  |
    iconv -t ISO88591 > pdfs/2101-AN-rattachement-2021.csv
  cat pdfs/2101-AN-rattachement-2021.html                               |
    grep 'data-sort'                                                    |
    tr '\n' ';'                                                         |
    sed -r 's|td data-sort="([^"]+)"><a href="/deputes/fiche/|\n\1;|g'  |
    sed  -r 's/[\t ;]*(<[^>]*>[\t ;]*)+/;/g'                            |
    sed -r 's/">|;</;/g'                                                |
    sed -r 's/;$//'                                                     |
    sed -r 's/^([^;]+);([^;]+);M[\.me]+ (.*) \1;(.*);$/\1;\3;\4;\2/'    |
    grep '[a-z]'                                                        |
    iconv -t ISO88591 >> pdfs/2101-AN-rattachement-2021.csv
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/sgp/Rattachements_partis_pol/Liste_nominative_rattachement_des_senateurs_pour_2021.pdf" -O pdfs/2012-Sénat-rattachement-2021.pdf
fi

# Complete CSV AN
bin/complete_an.py pdfs/2101-AN-rattachement-2021.csv > data/2101-AN-rattachement-2021.csv

# PDF Sénat
pdftohtml -xml pdfs/2012-Sénat-rattachement-2021.pdf > /dev/null
# the PDF is a scan for this year...
#bin/convert.py pdfs/2012-Sénat-rattachement-2021.xml 1
#bin/convert.py pdfs/2012-Sénat-rattachement-2021.xml > data/2012-Sénat-rattachement-2021.csv

# Build SQLs for ND/NS
bin/build_sql.sh data/2101-AN-rattachement-2021.csv
#bin/build_sql.sh data/2012-Sénat-rattachement-2021.csv

