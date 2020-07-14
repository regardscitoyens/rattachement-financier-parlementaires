#!/bin/bash

# AN https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000036145616&dateTexte=&categorieLien=id

CACHE=$1
if [ -z "$CACHE" ]; then
  wget -q --no-check-certificate "https://www.nosdeputes.fr/deputes/json" -O cache/deputes.json
  wget -q --no-check-certificate "https://www.nossenateurs.fr/senateurs/json" -O cache/senateurs.json
  wget -q "http://www2.assemblee-nationale.fr/deputes/liste/partis-politiques/(annee)/2020" -O pdfs/1912-AN-rattachement-2020.html
  echo "Nom_de_famille;ID_AN;Nom;Groupe;Parti ou groupement politique"  |
    iconv -t ISO88591 > pdfs/1912-AN-rattachement-2020.csv
  cat pdfs/1912-AN-rattachement-2020.html                               |
    grep 'data-sort'                                                    |
    tr '\n' ';'                                                         |
    sed -r 's|td data-sort="([^"]+)"><a href="/deputes/fiche/|\n\1;|g'  |
    sed  -r 's/[\t ;]*(<[^>]*>[\t ;]*)+/;/g'                            |
    sed -r 's/">|;</;/g'                                                |
    sed -r 's/;$//'                                                     |
    sed -r 's/^([^;]+);([^;]+);M[\.me]+ (.*) \1;(.*);$/\1;\3;\4;\2/'    |
    grep '[a-z]'                                                        |
    iconv -t ISO88591 >> pdfs/1912-AN-rattachement-2020.csv
  wget -q "http://www.senat.fr/fileadmin/Fichiers/Images/sgp/Rattachements_partis_pol/Liste_au_30_novembre_2019_pour_publication_01.pdf" -O pdfs/1912-Sénat-rattachement-2020.pdf
fi

# Complete CSV AN
bin/complete_an.py pdfs/1912-AN-rattachement-2020.csv > data/1912-AN-rattachement-2020.csv

# PDF Sénat
pdftohtml -xml pdfs/1912-Sénat-rattachement-2020.pdf > /dev/null
bin/convert.py pdfs/1912-Sénat-rattachement-2020.xml 1
bin/convert.py pdfs/1912-Sénat-rattachement-2020.xml > data/1912-Sénat-rattachement-2020.csv

# Build SQLs for ND/NS
bin/build_sql.sh data/1912-AN-rattachement-2020.csv
bin/build_sql.sh data/1912-Sénat-rattachement-2020.csv

