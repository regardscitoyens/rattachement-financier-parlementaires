#!/bin/bash

# AN https://www2.assemblee-nationale.fr/static/15/rattachement_partis/liste_rattachement_partis_2022.csv

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q --no-check-certificate "https://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q --no-check-certificate "https://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www2.assemblee-nationale.fr/deputes/liste/partis-politiques/(annee)/2022" -O pdfs/2111-AN-rattachement-2022.html
  echo "Nom_de_famille;ID_AN;Nom;Groupe;Parti ou groupement politique"  |
    iconv -t ISO88591 > pdfs/2111-AN-rattachement-2022.csv
  cat pdfs/2111-AN-rattachement-2022.html                               |
    grep 'data-sort'                                                    |
    tr '\n' ';'                                                         |
    sed -r 's|td data-sort="([^"]+)"><a href="/deputes/fiche/|\n\1;|g'  |
    sed  -r 's/[\t ;]*(<[^>]*>[\t ;]*)+/;/g'                            |
    sed -r 's/">|;</;/g'                                                |
    sed -r 's/;$//'                                                     |
    sed -r 's/^([^;]+);([^;]+);M[\.me]+ (.*) \1;(.*);$/\1;\3;\4;\2/'    |
    grep '[a-z]'                                                        |
    iconv -t ISO88591 >> pdfs/2111-AN-rattachement-2022.csv
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/sgp/Rattachements_partis_pol/liste_nominative_rattachement_des_senateurs_pour_2022.pdf" -O pdfs/2112-Sénat-rattachement-2022.pdf
fi

# Complete CSV AN
bin/complete_an.py pdfs/2111-AN-rattachement-2022.csv > data/2111-AN-rattachement-2022.csv

# PDF Sénat
pdftohtml -xml pdfs/2112-Sénat-rattachement-2022.pdf > /dev/null
bin/convert.py pdfs/2112-Sénat-rattachement-2022.xml 1
bin/convert.py pdfs/2112-Sénat-rattachement-2022.xml > data/2112-Sénat-rattachement-2022.csv

# Build SQLs for ND/NS
bin/build_sql.sh data/2111-AN-rattachement-2022.csv
bin/build_sql.sh data/2112-Sénat-rattachement-2022.csv

