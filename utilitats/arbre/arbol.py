#!/usr/bin/python3
# -*- coding: UTF8 -*-
'''
@author: rafael
@description: Reorganitzacio dels fitxers exportats dels projectes activityutil
'''
import os, sys

print("=================================================================")
print("reorganitzacio dels fitxers exportats dels projectes activityutil")
print("=================================================================")

#Valors per defecte
mdprojects="/home/rafael/projectes/data/mdprojects/activitats"
activity_dir="/home/rafael/projectes/data/ActivityUtil"
activity_base="documents_fp_docencia_activitats_"

#Tratamiento de los argumentos de la línea de comandos
arg = sys.argv[1:]
while arg:
	if (arg[0]=="-f" or arg[0]=="-file"):
		if (os.path.exists(arg[1]+".py")):
			params = __import__(arg[1])
			mdprojects = params.mdprojects
			activity_dir = params.activity_dir
			activity_base = params.activity_base
			break
		else:
			exit()
	elif (arg[0]=="-m" or arg[0]=="-mdprojects"):
		mdprojects = arg[1]
	elif (arg[0]=="-d" or arg[0]=="-activity_dir"):
		activity_dir = arg[1]
	elif (arg[0]=="-b" or arg[0]=="-activity_base"):
		activity_base = arg[1]
	elif (arg[0]=="-h" or arg[0]=="-help"):
		print("sintaxi:")
		print("-f <file>| -file <file>           : fitxer amb els paràmetres de configuració")
		print("-m <valor>| -mdprojects <valor>   : ruta absoluta de l'arbre de projectes a tractar")
		print("-d <valor>| -activity_dir <valor> : ruta absoluta de l'arbre de directoris FTP")
		print("-b <valor>| -activity_base <valor>: part del nom de directori corresponent als projectes")
		exit()
	arg = arg[2:]

#Número de elementos en la cadena mdprojects (usado en la función transformDir())
nmdp = len([c for c in mdprojects if c=="/"]) + 1

'''
Busca en el directorio activity_dir los directorios cuyo nombre contenga,
como parte del nombre, el valor project
Entonces crea un directorio de nombre project y mueve los directorios
encontrados a este nuevo directorio
A continuación crea unlaces simbólicos en activity_dir que apuntan a los
directorios anteriormente movidos
'''
def creaEstructura(project):
	listFiles = os.listdir(activity_dir)
	for file in listFiles:
		actual = file.replace(activity_base, "")
		if (actual.startswith(project)):
			origin = activity_dir+"/"+file
			new_dir = activity_dir+"/"+project+"/"
			destination = new_dir+file
			print("origen: "+origin+". destino: "+destination)
			if (not os.path.exists(new_dir)):
				os.mkdir(new_dir)
			os.rename(origin, destination)
			os.symlink(destination, origin)
	return

'''
Volta el directori mdprojects cencant projectes.
Les rutes -transformades- dels projectes son la base per a la
reorganitzacio dels fitxers exportats dels projectes activityutil
'''
def recorrido(rdir):

	def transformDir(sdir):
		spl = sdir.split("/")
		#eliminamos del array spl los 7 primeros elementos que corresponden a la variable mdprojects
		#y los 2 elementos finales: el nombre del directorio actual y el del fichero _wikiIocSystem_.mdpr
		spl = spl[nmdp:-2]
		return "_".join(spl)

	listProjects = os.listdir(rdir)

	for file in listProjects:
		actual = rdir+"/"+file
		if (os.path.isdir(actual)):
			recorrido(actual)
		else:
			if (file == "_wikiIocSystem_.mdpr"):
				project = transformDir(actual)
				print(project)
				creaEstructura(project)
	return

# ---
# main
# ----
recorrido(mdprojects)
print("=== FI ===")
