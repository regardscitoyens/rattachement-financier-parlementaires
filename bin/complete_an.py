#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, csv, json
sys.path.append('bin')
from common import clean, find_parl, unif_partis

filepath = sys.argv[1]
with open(filepath, 'r') as csv_file:
    csv = list(csv.DictReader(csv_file, delimiter=";"))

results = []
headers = ['nom', 'prénom', 'groupe', 'rattachement_parti', 'sexe', 'département', 'id_nosdeputes', 'url_institution']
record = ["", "", "", "", "", "", "", ""]

with open("cache/deputes.json") as f:
    parls = [p["depute"] for p in json.load(f)['deputes']]

for line in csv:
    for k in line:
        line[k] = (line[k] or "").decode('iso-8859-15').encode('utf-8')
    groupe = line["Groupe"].replace("app.", "").replace("Écolo", "ECOLO")
    parl = find_parl(line['Nom'], line.get('Pr\xe9nom', ''), groupe, parls)
    if not parl:
        print >> sys.stderr, "WARNING: could not process", line
        continue
    if ("-2019" in filepath or "-2020" in filepath) and not line['Parti ou groupement politique']:
        line['Parti ou groupement politique'] = line['Groupe']
        line['Groupe'] = ""
    results.append([
      line['Nom'],
      line.get('Pr\xe9nom', parl['prenom']),
      line['Groupe'],
      unif_partis(line['Parti ou groupement politique']),
      parl['sexe'],
      parl['nom_circo'],
      parl['slug'],
      parl['url_an']
    ])

print ",".join(['"%s"' % h for h in headers])
for i in results:
    for j in range(len(i)):
        i[j] = clean(i[j])
        try: i[j] = i[j].encode('utf-8')
        except: pass
    print ",".join([str(i[a]) if isinstance(i[a], int) else "\"%s\"" % i[a].replace('"', '""') for a,_ in enumerate(i)])

