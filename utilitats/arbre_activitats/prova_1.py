#!/usr/bin/python
# -*- coding: UTF8 -*-
import os, sys, socket

print(sys.version)

print("=====================================================")
print("Tratamiento de los argumentos de la línea de comandos")
print("=====================================================")

PREFIX="documents_fp_docencia_activitats_"
if (socket.gethostname() == "LM19"):
	MDPROJECTS="/home/rafael/Vídeos/mdprojects/activitats"
	PAGES="/home/rafael/Vídeos/pages/activitats"
	ACTIVITY_DIR="/home/rafael/Vídeos/ActivityUtil"
else:
	MDPROJECTS="/home/wikidev/wiki18/data/mdprojects/documents_fp/docencia/activitats/"
	PAGES="/home/wikidev/wiki18/data/pages/documents_fp/docencia/activitats/"
	ACTIVITY_DIR="."		#/html/FP/Recursos/ActivityUtil

#Tratamiento de los argumentos de la línea de comandos
arg = sys.argv[1:]
while arg:
	if (arg[0]=="-f" or arg[0]=="-file"):
		if (os.path.exists(arg[1]+".py")):
			print(arg[1]+".py")
			params = __import__(arg[1])
			MDPROJECTS = params.mdprojects
			ACTIVITY_DIR = params.activity_dir
			PREFIX = params.prefix
			break
		else:
			exit()
	elif (arg[0]=="-m" or arg[0]=="-mdprojects"):
		MDPROJECTS = arg[1]
	elif (arg[0]=="-d" or arg[0]=="-activity_dir"):
		ACTIVITY_DIR = arg[1]
	elif (arg[0]=="-b" or arg[0]=="-prefix"):
		PREFIX = arg[1]
	elif (arg[0]=="-h" or arg[0]=="-help"):
		print("sintaxi:")
		print("-f <file>| -file <file>           : fitxer amb els paràmetres de configuració")
		print("-m <valor>| -mdprojects <valor>   : ruta absoluta de l'arbre de projectes a tractar")
		print("-d <valor>| -activity_dir <valor> : ruta absoluta de l'arbre de directoris FTP")
		print("-b <valor>| -prefix <valor>       : part del nom de directori corresponent als projectes")
		exit()
	arg = arg[2:]

if (len(arg) == 0):
	print("No has indicat cap paràmetre, els paràmetres per defecte son:")
	print("  >> mdprojects   = " + MDPROJECTS)
	print("  >> activity_dir = " + ACTIVITY_DIR)
	print("  >> prefix       = " + PREFIX)
	r = raw_input("Vols continuar s/N: ")
	print(r.upper())

def transformDir2(dir, glue, **params):
        spl = dir.split("/")
        common_path = MDPROJECTS
        add_prefix = ""
        del_sufix = ""
        for key in params:
            if (key == 'common_path'): common_path = params[key]
            if (key == 'add_prefix'): add_prefix = params[key]
            if (key == 'del_sufix'): del_sufix = params[key]

        #eliminamos del array spl los nmdp primeros elementos que corresponden a la ruta common_path
        nmdp = len([c for c in common_path if c=="/"]) + 1
        spl = spl[nmdp:]
        ret = add_prefix + glue.join(spl)
        return ret.replace(del_sufix, "")

actual = "home/wikidev/wiki18/data/mdprojects/documents_fp/docencia/activitats/hiasrtiu.txt"
page_project = transformDir2(actual, "_", common_path=PAGES, add_prefix=PREFIX, del_sufix=".txt")
print(page_project)
