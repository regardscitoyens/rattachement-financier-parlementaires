#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, csv, json
sys.path.append('bin')
from common import clean, find_parl, unif_partis, checker, lowerize
from pprint import pprint

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

circosparls = {}
for parl in parls:
    try:
        circo = "%03d%02d" % (int(parl['num_deptmt']), int(parl['num_circo']))
    except:
        circo = "%s%02d" % (parl['num_deptmt'].upper(), int(parl['num_circo']))
    if circo not in circosparls:
        circosparls[circo] = []
    circosparls[circo].append(parl)

for circo, candidats in circos.items():
    parl = None
    for line in candidats:
        parl = find_parl(line['Nom candidat'], line['Prénom candidat'], None, circosparls[circo], silent=True)
        if parl:
            break

    if not parl:
        print >> sys.stderr, "WARNING: could not find député", ["%s | %s" % (checker(p["nom"]), p["groupe_sigle"]) for p in circosparls[circo]], "for circo", circo
        pprint(["%s | %s" % (checker("%s %s" % (p['Prénom candidat'], p['Nom candidat'])), p['Parti rattachement'].decode("utf-8")) for p in candidats], stream=sys.stderr)
        print >> sys.stderr
        parl = circosparls[circo][0]
        line['Nom candidat'] = parl["nom_de_famille"].upper()
        line['Prénom candidat'] = parl["prenom"]
        line['Parti rattachement'] = "Non rattaché%s" % ("e" if parl["sexe"] == "F" else "")
    results.append([
      line['Nom candidat'],
      line['Prénom candidat'],
      parl['groupe_sigle'],
      unif_partis(lowerize(line['Parti rattachement'])),
      parl['sexe'],
      parl['nom_circo'],
      parl['slug'],
      parl['url_an']
    ])
    del(circosparls[circo])

for circo, parls in circosparls.items():
    parl = parls[0]
    results.append([
      parl['nom_de_famille'].upper(),
      parl['prenom'],
      parl['groupe_sigle'],
      "Non rattaché%s" % ("e" if parl["sexe"] == "F" else ""),
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

