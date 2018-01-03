#!/bin/bash

# AN https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000036145616&dateTexte=&categorieLien=id

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q "http://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q "http://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www2.assemblee-nationale.fr/deputes/liste/partis-politiques/(annee)/2018" -O pdfs/1712-AN-rattachement-2018.html
  echo "Nom;Prénom;Groupe;Parti ou groupement politique;ID_AN"  |
    iconv -t ISO88591 > pdfs/1712-AN-rattachement-2018.csv
  cat pdfs/1712-AN-rattachement-2018.html                               |
    grep 'data-sort'                                                    |
    tr '\n' ';'                                                         |
    sed -r 's|td data-sort="([^"]+)"><a href="/deputes/fiche/|\n\1;|g'  |
    sed  -r 's/[\t ;]*(<[^>]*>[\t ;]*)+/;/g'                            |
    sed -r 's/">|;</;/g'                                                |
    sed -r 's/^([^;]+);([^;]+);M[\.me]+ (.*) \1;(.*);$/\1;\3;\4;\2/'    |
    grep '[a-z]'                                                        |
    iconv -t ISO88591 >> pdfs/1712-AN-rattachement-2018.csv
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/sgp/Rattachements_partis_pol/Liste_rattachements_pour_2018.pdf" -O pdfs/1712-Sénat-rattachement-2018.pdf
fi

# Complete CSV AN
bin/complete_an.py pdfs/1712-AN-rattachement-2018.csv > data/1712-AN-rattachement-2018.csv

# PDF Sénat
pdftohtml -xml pdfs/1712-Sénat-rattachement-2018.pdf > /dev/null
bin/convert.py pdfs/1712-Sénat-rattachement-2018.xml 1
bin/convert.py pdfs/1712-Sénat-rattachement-2018.xml > data/1712-Sénat-rattachement-2018.csv

# Build SQLs for ND/NS
bin/build_sql.sh data/1712-AN-rattachement-2018.csv
bin/build_sql.sh data/1712-Sénat-rattachement-2018.csv

