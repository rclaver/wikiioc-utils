#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 20:31:39 2025
@author: rafael
@description: Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24
"""

import json, re

# Taula de equivalències ("original LOE": "destí LOE24")
taulaEquiv = {
    "nsProgramacio": "nsProgramacio",
    "nouCurr": "nouCurr",
    "pesPAFnouCurr": "pesPAFnouCurr",
    "semestre": "semestre",
    "tipusBlocModul": "tipusBlocModul",
    "cicle": "cicle",
    "modulId": "modulId",
    "modul": "modul",
    "durada": "durada",
    "duradaCicle": "duradaCicle",
    "professors": "professors",
    "coordinador": "coordinador",
    "urlMaterialDidactic": "urlMaterialDidactic",
    "dedicacio": "dedicacio",
    "requerimentsMatricula": "requerimentsMatricula",
    "descripcio": "descripcio",
    "itinerarisRecomanats": "itinerarisRecomanats",
    "taulaDadesUF": "taulaDadesUn",
    "taulaDadesUnitats": "taulaUnitatRAs",
    "einesAprenentatge": "einesAprenentatge",
    "resultatsAprenentatge": "resultatsAprenentatge",
    "activitatsAprenentatge": "activitatsAprenentatge",
    "avaluacioInicial": "avaluacioInicial",
    "calendari": "calendari",
    "datesAC": "datesAC",
    "hiHaSolucioPerAC": "hiHaSolucioPerAC",
    "datesEAF": "datesEAF",
    "treballEquipEAF": "treballEquipEAF",
    "hiHaSolucioPerEAF": "hiHaSolucioPerEAF",
    "hiHaEnunciatRecuperacioPerEAF": "hiHaEnunciatRecuperacioPerEAF",
    "hiHaRecuperacioPerJT": "hiHaRecuperacioPerJT",
    "datesJT": "datesJT",
    "notaMinimaAC": "notaMinimaAC",
    "notaMinimaEAF": "notaMinimaEAF",
    "notaMinimaJT": "notaMinimaJT",
    "dataPaf11": "dataPaf11",
    "dataPaf12": "dataPaf12",
    "dataPaf21": "dataPaf21",
    "dataPaf22": "dataPaf22",
    "dataQualificacioPaf1": "dataQualificacioPaf1",
    "dataQualificacioPaf2": "dataQualificacioPaf2",
    "notaMinimaPAF": "notaMinimaPAF",
    "dadesQualificacioUFs": "dadesQualificacioUns",
    "duradaPAF": "duradaPAF",
    "dadesExtres": "dadesExtres",
    "plantilla": "plantilla",
    "autor": "autor",
    "responsable": "responsable",
    "supervisor": "supervisor",
    "fitxercontinguts": "fitxercontinguts",
    "moodleCourseId": "moodleCourseId",
    "dataFromMix": "dataFromMix"
}
# canvi de nom
taulaDadesUF = {
   "bloc": "bloc",
   "unitat formativa": "unitat",
   "nom": "nom",
   "ordreImparticio": "ordreImparticio",
   "hores": "hores",
   "ponderaci\\u00f3": "ponderaci\\u00f3"
}
taulaDadesUnitats = {
   "unitat formativa": "unitat",
   "unitat": "RA",
   "nom": "",
   "hores": ""
}
dadesQualificacioUFs = {
   "unitat formativa": "unitat",
   "tipus qualificació": "tipus qualificació",
   "descripció qualificació": "descripció qualificació",
   "abreviació qualificació": "abreviació qualificació",
   "ponderaci\\u00f3": "ponderaci\\u00f3"
}

"""
Llegeix l'arxiu mdpr, fragmenta la cadena json obtinguda truncant amb ","
i guarda els elements en format array a 'arrayOrigen'
"""
def processarArxiuDades():
    arxiuMdpr = "~/projectes/wiki18/data/mdprojects/docs/loe_1/ptfploe/meta.mdpr"
    if (os.path.exists(arxiuMdpr)):
        contingut = open(arxiuMdpr).read()
        dadesJson = json.loads(contingut)
        return true
    else:
        print("Arxiu no trobat")
        return false





print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if processarArxiuDades():
