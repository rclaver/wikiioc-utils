#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 20:31:39 2025
@author: rafael
@description: Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24
"""

import json, os

arxiuMdpr = "/home/rafael/Escritorio/meta.mdpr"

# Taula de equivalències ("original LOE": "destí LOE24")
taulaEquiv = {
    "taulaDadesUF": "taulaDadesUn",
    "taulaDadesUnitats": "taulaUnitatRAs",
    "dadesQualificacioUFs": "dadesQualificacioUns",
}
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
Llegeix l'arxiu mdpr i retorna una estructura json
"""
def carregaArxiuMdpr(arxiu):
   if (os.path.exists(arxiu)):
      contingut = open(arxiu).read()
      return json.loads(contingut)
   else:
      print("Arxiu no trobat")
      return False

"""
Verifica si el valor donat és un json
"""
def isJson(data):
   if (isinstance(data, dict)):
      return True
   elif (isinstance(data, int) or data.isnumeric()):
      return False
   else:
      try:
         json.loads(data)
      except (ValueError, TypeError):
         return False
      return True

"""
Verifica si existeix la variable donada
"""
def existeix(var):
   return eval(var) if var in globals() else None

"""
Transforma una List en un Dict
"""
def transListToDict(value):
   if (value or len(value) > 0 or value != None):
      value = json.loads(value)
      if (isinstance(value, list)):
         d = {}
         for i in value:
            d.update(i)
         value = d
   return value

"""
 Cerca a la Taula d'equivalències 'taulaEquiv' la parella que conté
 la clau origen i retorna la parella associada
"""
def cercaTaulaEquiv(origen):
   desti = taulaEquiv.get(origen)
   return desti if desti else origen

"""
 Cerca a la taula d'equivalències indicada la parella que conté
 la clau origen i retorna la parella associada
"""
def cercaEquiv(taula, origen):
   desti = taula.get(origen)
   return desti

"""
 Procés principal
"""
def process(dades, arrayTrans=None):
   parcial = {}

   for key, value in dades.items():
      if (not arrayTrans):
         arrayTrans = existeix(key)
         keyTrans = cercaTaulaEquiv(key)
      else:
         keyTrans = cercaEquiv(arrayTrans, key)

      if (not isJson(value)):
         # afegeix un nou element al json
         parcial[keyTrans] = value
      else:
         if (not value or len(value) == 0 or value == None):
            parcial[keyTrans] = value
         else:
            if (not isinstance(value, dict)):
               value = transListToDict(value)
            parcial[keyTrans] = process(value, arrayTrans)


   return parcial

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

dadesJson = carregaArxiuMdpr(arxiuMdpr)
if (dadesJson):
   jmain = process(dadesJson)
   jsonFinal = {"main": jmain}
   print(jsonFinal)
