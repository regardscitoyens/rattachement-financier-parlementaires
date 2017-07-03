#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, csv, json
sys.path.append('bin')
from common import clean, find_parl, unif_partis

filepath = sys.argv[1]
with open(filepath, 'r') as csv_file:
    csv = list(csv.DictReader(csv_file, delimiter=","))

results = []
headers = ['nom', 'prénom', 'groupe', 'rattachement_parti', 'sexe', 'département', 'id_nosdeputes', 'url_institution']
record = ["", "", "", "", "", "", "", ""]

with open("cache/deputes.json") as f:
    parls = [p["depute"] for p in json.load(f)['deputes']]

circos = {}
for line in csv:
    circo = line["code circo"]
    if circo not in circos:
        circos[circo] = []
    circos[circo].append(line)

for circo, candidats in circos.items():
    parl = None
    for line in candidats:
        parl = find_parl(line['Nom candidat'], line['Prénom candidat'], None, parls, circo)
        if parl:
            break

    if not parl:
        print >> sys.stderr, "WARNING: could not find député for circo %s" % circo
        print >> sys.stderr, candidats
        print >> sys.stderr
        continue
    results.append([
      line['Nom candidat'],
      line['Prénom candidat'],
      parl['groupe_sigle'],
      unif_partis(line['Parti rattachement']),
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

