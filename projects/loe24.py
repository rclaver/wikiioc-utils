#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 20:31:39 2025
@author: rafael
@description: Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24
"""

import json, os

llistaArxius = "llistaPTLOE.txt"
#arxiuMdprLOE = "/home/rafael/Escritorio/meta.mdpr"
#arxiuMdprLOE24 = "/home/rafael/Escritorio/meta24.mdpr"

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
   "ponderació": "ponderació",
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
   "ponderació": "ponderació",
   "ponderaci\\u00f3": "ponderaci\\u00f3"
}

def obteLlistaArxius():
   global llistaArxius
   if (os.path.exists(llistaArxius)):
      llista = open(llistaArxius).read()
      return json.loads(llista)
   else:
      print("No he trobar el fitxer \'${llistaArxius}\' que conté la llista d'arxius")
      return False


"""
Llegeix l'arxiu mdpr i retorna una estructura json
"""
def carregaArxiuMdprLOE(arxiu):
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
   elif (data == "false" or data == "False" or data == "true" or data == "True"):
      return False
   else:
      try:
         json.loads(data)
      except (ValueError, TypeError):
         return False
      return True

"""
Verifica si existeix la variable donada. Si existeix retorna aquesta variable
"""
def existeix(var):
   return eval(var) if var in globals() else None

"""
Transforma ' en " y elimina espais
"""
def maqueado(value):
   # elimina espais
   value = value.replace(": ", ":")
   value = value.replace(", ", ",")
   # canvia cometes simples per dobles
   value = value.replace("{'", "{\"")
   value = value.replace("'}", "\"}")
   value = value.replace("':'", "\":\"")
   value = value.replace("','", "\",\"")
   value = value.replace("':", "\":")
   # elimina caracters duplicats
   value = value.replace("\\\\\"", "\\\"")
   value = value.replace("\\\\\\\\", "\\\\")
   value = value.replace("\"\"[", "\"[")
   value = value.replace("]\"\"", "]\"")
   return value

"""
Transforma un String en List
"""
def transStringToList(value):
   value = json.loads(value)
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
         #si existeix, obté la taula d'equivalències indicada a 'key'
         arrayTrans = existeix(key)
         keyTrans = cercaTaulaEquiv(key)
      else:
         keyTrans = cercaEquiv(arrayTrans, key)

      if (not isJson(value)):
         parcial[keyTrans] = value
      else:
         if (not value or len(value) == 0 or value == None or value == "[]" ):
            parcial[keyTrans] = value
         else:
            if (not isinstance(value, dict)):
               value = transStringToList(value)
               print(type(value), value)
               p = "["
               for e in value:
                  print(e)
                  p += json.dumps(process(e, arrayTrans)) + ","
               p += "]"
               print(type(p), p)
               parcial[keyTrans] = json.dumps(p)
            else:
               parcial[keyTrans] = process(value, arrayTrans)
         arrayTrans = None

   return parcial

"""
bucle principal per a tots els arxius consignats a la llista d'arxius
"""
def inici():
   llista = obteLlistaArxius()
   if (llista):
      for key in llista:
         dades = carregaArxiuMdprLOE(key)
         if (dades):
            trans = process(dades)
            trans = maqueado(str(trans))
            with open(llista[key], "w") as f:
               f.write(trans)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Importació de dades d'un pla de treball LOE a un nou pla de treball LOE24")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

inici()

#dadesJson = carregaArxiuMdprLOE(arxiuMdprLOE)
#if (dadesJson):
#   jsonFinal = process(dadesJson)
#   print(jsonFinal)
#   with open(arxiuMdprLOE24, "w") as f:
#      f.write(str(jsonFinal))
