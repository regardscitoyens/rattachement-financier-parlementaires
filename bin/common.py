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
    (u'[ôÔÖöÔ]', 'o'),
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

re_mme = re.compile(r'^M(me|\.)\s+', re.I)
def find_parl(nom, prenom, groupe, parls, silent=False):
    res = []
    prenom = checker(prenom)
    nom = checker(nom)
    nom = re_mme.sub('', nom)
    nom = nom.replace(u"leborgn'", u"le borgn'")
    nom = nom.replace(u"rihan-cypel", u"rihan cypel")
    nom = nom.replace(u"d’artagnan", u"de montesquiou")
    nom = nom.replace(u"morel-a-lhuissier",  u"morel-a-l'huissier")
    if nom == "vogel":
        prenom = prenom.replace(u"jean-pierre",  u"jean pierre")
    nom_complet = ("%s %s" % (prenom, nom)).strip()
    nom_complet = nom_complet.replace(u"jean-baptiste djebbari-bonnet", u"jean-baptiste djebbari")
    nom_complet = nom_complet.replace(u"philippe-michel kleisbauer", u"philippe michel-kleisbauer")
    nom_complet = nom_complet.replace(u"mostapha laabid", u"mustapha laabid")
    nom_complet = nom_complet.replace(u"liliane tanguy", u"liliana tanguy")
    nom_complet = nom_complet.replace(u"moeta brotherson", u"moetai brotherson")
    nom_complet = nom_complet.replace(u"jean hugues ratenon", u"jean-hugues ratenon")
    nom_complet = nom_complet.replace(u"amal amelia lakrafi", u"amal-amelia lakrafi")
    nom_complet = nom_complet.replace(u"nicole gries-trisse", u"nicole trisse")
    nom_complet = nom_complet.replace(u"claire javois", u"claire guion-firmin")
    nom_complet = nom_complet.replace(u"anne laure cattelot", u"anne-laure cattelot")
    nom_complet = nom_complet.replace(u"pierre morel a l'huissier", u"pierre morel-a-l'huissier")
    for parl in parls:
        if checker(parl['nom']) == nom_complet or (checker(parl['nom_de_famille']) == nom and checker(parl['prenom']) == prenom):
            return parl
        if (groupe and checker(parl['nom_de_famille']) == nom and parl['groupe_sigle'] == groupe) \
          or (checker(parl['prenom']) == prenom and checker(parl['nom_de_famille']).startswith(nom)):
            res.append(parl)
    if not res:
        if not silent:
            sys.stderr.write("Could not find %s\n" % nom_complet)
        return None
    if len(res) > 1:
        sys.stderr.write("Found too many %s : %s\n" % (nom_complet, res))
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
    p = p.replace('Mouvement démocrate', 'Mouvement Démocrate')
    p = p.replace('France insoumise', 'France Insoumise')
    p = p.replace('La République en marche', 'En marche !')
    p = p.replace('Non déclaré', 'Non rattaché')
    p = p.replace('Non rattaché(s)', 'Non rattaché')
    p = p.replace('Aucun parti', 'Non rattaché')
    p = p.replace(' (URCID)', '')
    p = p.replace('Union de la majorité municipale', 'La politique autrement (Union de la majorité municipale)') if p.startswith('Union') else p
    p = p.replace('PSLE-Nouveau', 'PSLE Nouveau')
    p = p.replace("Tavini Huiraatira no te ao ma'ohi (Front de libération de Polynésie)", "Front de libération de la Polynésie - Tavini Huiraatira no te ao ma'ohi")
    p = p.replace('radicaux centristes', 'radicaux, centristes')
    p = p.replace('radicaux, centristes, indépendants et démocrates', 'Radicaux, Centristes, Indépendants et Démocrates')
    p = p.replace('Les Républicains Union pour un Mouvement Populaire)', 'Les Républicains (Union pour un Mouvement Populaire)')
    return p

re_word_to_lower = re.compile(ur"(^| |')([A-ZÉ])([A-ZÉ]+)")
def lowerize(s):
    return re_word_to_lower.sub(lambda x: x.group(1) + x.group(2) + x.group(3).lower(), s.decode("utf-8")).encode("utf-8")

