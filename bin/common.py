#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

re_clean_bal = re.compile(r'<[^>]+>')
re_clean_spaces = re.compile(r'\s+')

clean = lambda x: re_clean_spaces.sub(' ', re_clean_bal.sub('', x)).strip()

regexps = [(re.compile(r), s) for r, s in [
    (u'[àÀ]', 'a'),
    (u'[éÉèÈêÊëË]', 'e'),
    (u'[îÎïÏ[]', 'i'),
    (u'[ôÔöÔ]', 'o'),
    (u'[ùÙûÛüÜ]', 'u'),
    (u'[çÇ]', 'c'),
]]

def clean_accents(t):
    if not isinstance(t, unicode):
        t = t.decode('utf-8')
    for r, s in regexps:
        t = r.sub(s, t)
    return t

checker = lambda x: clean(clean_accents(x)).lower().strip()

def find_parl(nom, prenom, groupe, parls):
    res = []
    prenom = checker(prenom)
    nom = checker(nom)
    nom = nom.replace("leborgn'", "le borgn'")
    nom = nom.replace("rihan-cypel", "rihan cypel")
    nom = nom.replace(u"d’artagnan", u"de montesquiou")
    nom = nom.replace(u"morel-a-lhuissier",  u"morel-a-l'huissier")
    if nom == "vogel":
        prenom = prenom.replace(u"jean-pierre",  u"jean pierre")
    for parl in parls:
        if checker(parl['nom']) == "%s %s" % (prenom, nom) or (checker(parl['nom_de_famille']) == nom and checker(parl['prenom']) == prenom):
            return parl
        if (checker(parl['nom_de_famille']) == nom and parl['groupe_sigle'] == groupe) or (checker(parl['prenom']) == prenom and checker(parl['nom_de_famille']).startswith(nom)):
            res.append(parl)
    if not res:
        sys.stderr.write("Could not find %s %s\n" % (prenom, nom))
        return None
    if len(res) > 1:
        sys.stderr.write("Found too many %s %s : %s\n" % (prenom, nom, res))
    return res[0]

def unif_partis(p):
    p = p.replace('et réalités', 'et Réalité')
    p = p.replace('Front national', 'Front National')
    p = p.replace('les Verts', 'Les Verts')
    p = p.replace('Ecologie', 'Écologie')
    p = p.replace("Indépendants de la France de métropole et d'Outre ", "Les Indépendants de la France métropolitaine et d'Outre-")
    p = p.replace('écologie les', 'Écologie Les')
    for w in ['Français', 'Huiraatira', 'Réunion', 'Mouvement', 'Populaire', 'Indépendantiste', 'Martiniquais' ,'Ensemble', 'République', 'Unie', 'Socialisme', 'Outre-mer', 'Réalité']:
        p = p.replace(w.lower(), w)
    p = p.replace('Non déclaré', 'Non rattaché')
    p = p.replace('Aucun parti', 'Non rattaché')
    p = p.replace(' (URCID)', '')
    p = p.replace('Union de la majorité municipale', 'La politique autrement (Union de la majorité municipale)') if p.startswith('Union') else p
    p = p.replace('PSLE-Nouveau', 'PSLE Nouveau')
    p = p.replace("Tavini Huiraatira no te ao ma'ohi (Front de libération de Polynésie)", "Front de libération de la Polynésie - Tavini Huiraatira no te ao ma'ohi")
    p = p.replace('radicaux centristes', 'radicaux, centristes')
    p = p.replace('radicaux, centristes, indépendants et démocrates', 'Radicaux, Centristes, Indépendants et Démocrates')
    p = p.replace('Les Républicains Union pour un Mouvement Populaire)', 'Les Républicains (Union pour un Mouvement Populaire)')
    return p


