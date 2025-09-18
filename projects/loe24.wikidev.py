#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 20:31:39 2025
@author: rafael
@description: Duplica un pla de treball LOE i transforma les dades en un projecte LOE24

@parameters:
   - l'arxiu que conté les dades s'ha d'anomenar: "llistaPTLOE.txt"
   - l'arxiu ha d'estar en format JSON
   - cada 'key' conté el nom d'un projecte LOE existent que es vol duplicar en una versió LOE24
   - cada 'value' conté el nou nom pel nou projecte LOE24 que s'ha de generar
   - exemple: {"pt_asx_m03b1_orig":"pt_asx_m03b1"}
   - tots els arxius -original LOE i còpia LOE24- s'han de trobar a:
      "/home/dokuwiki/wiki18/data/[mdprojects|media|pages]/documents_fp/plans_de_treball"
"""

import json, os, shutil

dirBase0 = "/home/wikidev/wiki18"
dirBase1 = f"{dirBase0}/data"
dirBase2 = "documents_fp/plans_de_treball"

arxiuMdpr = "meta.mdpr"
dirMdp = "mdprojects"
dataDir = [dirMdp,"media","pages"]
tipusProjecteLoe = "ptfploe"
tipusProjecteLoe24 = "ptfploe24"
continguts = f"{dirBase0}/lib/plugins/wikiiocmodel/projects/ptfploe24/metadata/plantilles/continguts.txt"
llistaProjectes = "llistaPTLOE.txt"

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

def obteLlistaProjectes():
   global llistaProjectes
   if (os.path.exists(llistaProjectes)):
      llista = open(llistaProjectes).read()
      return json.loads(llista)
   else:
      print("No he trobar el fitxer", llistaProjectes, "que conté la llista de projectes")
      return False

"""
Duplica el projecte LOE fent veure que la còpia és del tipus LOE24
"""
def duplicaProjecte(pLoe, pLoe24):
   if (verificaProjecte(pLoe, pLoe24)):
      for dd in dataDir:
         dataDirLoe = f"{dirBase1}/{dd}/{dirBase2}/{pLoe}"
         dataDirLoe24 = f"{dirBase1}/{dd}/{dirBase2}/{pLoe24}"
         if (dd == dirMdp):
            dataDirLoe += "/"+tipusProjecteLoe
            dataDirLoe24 += "/"+tipusProjecteLoe24

         # crea el directori pel nou projecte LOE24
         os.makedirs(dataDirLoe24, 0o777)

         # copia el contingut del directori LOE al nou directori LOE24
         if (dd == "pages"):
            shutil.copyfile(continguts, f'{dataDirLoe24}/continguts.txt')
         else:
            dirlist = os.listdir(dataDirLoe)
            for f in dirlist:
               shutil.copyfile(f"{dataDirLoe}/{f}", f'{dataDirLoe24}/{f}')

      return True
   else:
      return False


"""
Verifica que el projecte LOE existeix, està sencer i elimina, si existeixen, els corresponents directoris LOE24
"""
def verificaProjecte(pLoe, pLoe24):
   for dd in dataDir:
      dataDirLoe = f"{dirBase1}/{dd}/{dirBase2}/{pLoe}"
      dataDirLoe24 = f"{dirBase1}/{dd}/{dirBase2}/{pLoe24}"
      if (not os.path.exists(dataDirLoe)):
         print("error:", dataDirLoe, "no existeix")
         return False

      if (os.path.exists(dataDirLoe24)):
         print("Atenció: el directori", dataDirLoe24, "ja existeix. Procedim a eliminar-lo")
         eliminaDirectori(dataDirLoe24)

   return True

"""
Elimina recursivament un directori
"""
def eliminaDirectori(dir):
   dirlist = os.listdir(dir)
   for f in dirlist:
      arxiu = f"{dir}/{f}"
      if (os.path.isdir(arxiu)):
         eliminaDirectori(arxiu)
      else:
         os.remove(arxiu)

   os.rmdir(dir)

"""
Llegeix l'arxiu mdpr i retorna una estructura json
"""
def carregaArxiuMdprLOE(pLoe):
   arxiu = f"{dirBase1}/{dirMdp}/{dirBase2}/{pLoe}/{tipusProjecteLoe}/meta.mdpr"
   if (os.path.exists(arxiu)):
      contingut = open(arxiu).read()
      return json.loads(contingut)
   else:
      print("Arxiu", arxiu, "no trobat")
      return False

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
   value = value.replace(",'", ",\"")
   value = value.replace("':", "\":")
   # elimina caracters duplicats
   value = value.replace("\\\\", "\\")
   value = value.replace("\"\"[", "\"[")
   value = value.replace("]\"\"", "]\"")
   return value

"""
Verifica si el valor donat és un json
"""
def isJson(data):
   if (isinstance(data, dict)):
      return True
   elif (isinstance(data, int)):
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
   return desti if desti else origen

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


      if (not isJson(value) or len(value) == 0 or value == None or value == "[]"):
         parcial[keyTrans] = value
      else:
         if (isinstance(value, dict)):
            parcial = process(value, arrayTrans)
         else:
            value = json.loads(value)
            p = "["
            for k in value:
               pk = process(k, arrayTrans)
               p += json.dumps(pk) + ","
            p = p.rstrip(",") + "]"
            p = p.replace('"', '\\"')
            parcial[keyTrans] = '\"' + p + '\"'

         arrayTrans = None

   return parcial

"""
bucle principal per a tots els arxius consignats a la llista d'arxius
"""
def inici():
   llista = obteLlistaProjectes()
   print("llista de projectes", llista)
   if (llista):
      for projectLoe in llista:
         projectLoe24 = llista[projectLoe]
         print("PROJECTE actual:", projectLoe, "-", projectLoe24)
         if (duplicaProjecte(projectLoe, projectLoe24)):
            dades = carregaArxiuMdprLOE(projectLoe)
            if (dades):
               trans = process(dades)
               trans = maqueado(str(trans))
               nouJson = '{"main":' + trans + '}'
               nouArxiuMdpr24 = f"{dirBase1}/{dirMdp}/{dirBase2}/{projectLoe24}/{tipusProjecteLoe24}/meta.mdpr"
               with open(nouArxiuMdpr24, "w") as f:
                  f.write(nouJson)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(" Creació de nous plans de treball LOE24")
print(" important les dades de plans de treball LOE")
print(" i transformant-les al nou model LOE24")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

inici()
