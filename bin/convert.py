#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, json
sys.path.append('bin')
from common import clean, find_parl, unif_partis

filepath = sys.argv[1]
with open(filepath, 'r') as xml_file:
    xml = xml_file.read()

drawMap = False
if len(sys.argv) > 2:
    drawMap = True

filterallpages = False
minl = 0
minfont = 0
if "-AN-" in filepath:
    typeparl = "depute"
    if "-2013" in filepath:
        mint = 200
        maxt = 670
        lastp = 12
        l3 = 500
    elif "-2014" in filepath:
        mint = 110
        maxt = 950
        lastp = 11
        l3 = 375
    l1 = 50
    l2 = 250
elif "-Sénat-" in filepath:
    typeparl = "senateur"
    lastp = "all"
    l2 = 300
    if "-2013" in filepath:
        filterallpages = True
        mint = 155
        maxt = 1190
        minl = 120
        l2 = 400
    elif "-2014" in filepath:
        mint = 200
        maxt = 1100
    elif "-2015" in filepath:
        minfont = 2
        mint = 150
        maxt = 1150
    l1 = 200
    l3 = 475

with open("cache/%ss.json" % typeparl, 'r') as f:
    parls = [p[typeparl] for p in json.load(f)['%ss' % typeparl]]

re_gpe = re.compile(r' (UMP|SOC)$')
re_app = re.compile(r'^\s*(app|ratt)[.\s]*', re.I)
clean_app = lambda x: re_app.sub('', x)

re_particule = re.compile(r"^(.*)\s+\((d[eu'\sla]+)\)\s*$")
clean_part = lambda x: re_particule.sub(r'\2 \1', x).replace("' ", "'").replace('  ', ' ')


page = 0
topvals = {}
leftvals = {}
maxtop = 0
maxleft = 0
results = []
headers = ['nom', 'prénom', 'groupe', 'rattachement_parti', 'sexe', 'département', 'id_nos%ss' % typeparl, 'url_institution']
record = ["", "", "", "", "", "", "", ""]
re_line = re.compile(r'<page number|text top="(\d+)" left="(\d+)"[^>]*font="(\d+)">(.*)</text>', re.I)
for line in (xml).split("\n"):
    #print "DEBUG %s" % line
    if line.startswith('<page'):
        page += 1
    if not line.startswith('<text'):
        continue
    attrs = re_line.search(line)
    if not attrs or not attrs.groups():
        raise Exception("WARNING : line detected with good font but wrong format %s" % line)
    text = attrs.group(4).replace("&amp;", "&")
    if not text.strip():
        continue
    font = int(attrs.group(3))
    if font < minfont:
        continue
    top = int(attrs.group(1))
    if top > maxtop:
        maxtop = top
    if not font in topvals:
        topvals[font] = []
    topvals[font].append(top)
    left = int(attrs.group(2))
    if left > maxleft:
        maxleft = left
    if not font in leftvals:
        leftvals[font] = []
    leftvals[font].append(left)
    if drawMap:
        continue
    #print "DEBUG %s %s %s %s" % (font, left, top, text)
    if ((page == 1 or filterallpages) and top < mint) or ((lastp == "all" or page == lastp) and top > maxt):
        continue
    if left < minl:
        continue
    if left < l1:
        record[0] = clean_part(clean(text))
    elif left < l2:
        record[1] = clean(text)
        match = re_gpe.search(record[1])
        if match:
            record[1] = re_gpe.sub('', record[1]).strip()
            record[2] = match.group(1).strip()
    elif left < l3:
        if "<b>" in text:
            a = text.split(' <b>')
            record[2] = a[0]
            record[3] = a[1]
        else:
            record[2] = clean(text)
        record[2] = clean_app(record[2]).replace("Rassemblement-", "R").replace("ÉCOL.", 'ECOLO').replace('Ecolo', 'ECOLO')
    else:
        record[3] = clean(text)
    if record[3]:
        if not "".join(record[:2]):
            tmp = clean(record[3])
            record = results.pop()
            record[3] = "%s %s" % (clean(record[3]), tmp)
        record[3] = unif_partis(record[3])
        parl = find_parl(record[0], record[1], record[2], parls)
        if parl:
            record[4] = parl.get('sexe').encode('utf-8')
            record[5] = parl.get('nom_circo').encode('utf-8')
            record[6] = parl.get('slug').encode('utf-8')
            record[7] = parl.get('url_institution', parl.get('url_an')).encode('utf-8')
        results.append(record)
        record = ["", "", "", "", "", "", "", ""]

if not drawMap:
    print ",".join(['"%s"' % h for h in headers])
    for i in results:
        for j in range(len(i)):
            i[j] = clean(i[j])
        print ",".join([str(i[a]) if isinstance(i[a], int) else "\"%s\"" % i[a].replace('"', '""') for a,_ in enumerate(i)])

else:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import cm

    fig = plt.figure(figsize=(8.5, 12))
    ax = fig.add_subplot(111)
    ax.grid(True, fillstyle='left')
    nf = len(leftvals)
    for font in leftvals:
        color = cm.jet(1.5*font/nf)
        ax.plot(leftvals[font], topvals[font], 'ro', color=color, marker=".")
        plt.figtext((font+1.)/(nf+1), 0.95, "font %d" % font, color=color)
    plt.xticks(np.arange(0, maxleft + 50, 50))
    plt.yticks(np.arange(0, maxtop + 50, 50))
    plt.xlim(0, maxleft + 50)
    plt.ylim(0, maxtop + 50)
    plt.gca().invert_yaxis()
    mappath = filepath.replace(".xml", ".png").replace("pdfs/", "pdfmaps/")
    fig.savefig(mappath)
    fig.clf()
    plt.close(fig)

