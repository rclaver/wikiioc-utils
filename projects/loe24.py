#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 20:31:39 2025
@author: rafael
@description: Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24
"""

import json, re, os

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
Llegeix l'arxiu mdpr i crea un json a 'dadesJson'
"""
def processarArxiuDades(arxiu):
   global dadesJson
   if (os.path.exists(arxiu)):
      contingut = open(arxiu).read()
      dadesJson = json.loads(contingut)
      return True
   else:
      print("Arxiu no trobat")
      return False

"""
 Cerca a la Taula d'equivalències 'taulaEquiv' la parella que conté
 la clau origen sol·licitada i retorna la parella associada
"""
def cercaEquiv(origen):
   desti = taulaEquiv[origen]
   return desti

"""
 Afegeix un nou element a la cadena de sortida 'jsonFinal' prèvia transformació de l'origen en destí
"""
def processaJsonFinal(key, value):
   global jsonFinal
   trans = cercaEquiv(key)
   jsonFinal += '\"' + trans + '\":' + value + ','


def processaJsonParcial(cadenaComp):
   jstring = json.loads(cadenaComp)

"""
 Procés principal: tractament de tots els elements de l'arrayOrigen
"""
def proces():
   global dadesJson
   iComp = 0  #indicador de 'valor' compost (conté sub-elements json)
   claud = 0  #indicador de nivell de sub-element json (nombre de claudàtors oberts)

   for key, value in dadesJson:
      if (iComp == 0):
         # la part 'valor' és una cadena simple sense sub-elements json
         if (value == '"[]"'):
            processaJsonFinal(key, value)
         elif (value[0] != "["):
            processaJsonFinal(key, value)
         else:
            iComp = 1
            claud+= 1
            cadenaComp = "${e},"
      else:
         #la part 'valor' és part d'una cadena composta (conté sub-elements json)
         cadenaComp += "${e},"
         if (value[0] == "["):
            claud += 1
         elif (value[-1] == "]"):
            claud -= 1
            if (claud == 0):
               cadenaComp = cadenaComp[:-1]   #elimina la coma final
               processaJsonParcial(cadenaComp)
               iComp = 0


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

arxiuMdpr = "~/projectes/wiki18/data/mdprojects/docs/loe_1/ptfploe/meta.mdpr"
jsonFinal = '{"main":{'

if processarArxiuDades(arxiuMdpr):
   proces()
