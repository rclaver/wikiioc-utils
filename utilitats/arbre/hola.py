#!/usr/bin/python3
# -*- coding: UTF8 -*-
import os, sys

print("=====================================================")
print("Tratamiento de los argumentos de la línea de comandos")
print("=====================================================")

mdprojects=""
activity_dir=""
activity_base=""

#Tratamiento de los argumentos de la línea de comandos
arg = sys.argv[1:]
while arg:
	if (arg[0]=="-f" or arg[0]=="-file"):
		if (os.path.exists(arg[1]+".py")):
			print(arg[1]+".py")
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
print(f"{nmdp = }")

print(f"argumentos recibidos: {sys.argv[1:] = }")
print("argumentos tratados:")
print(f"{mdprojects = }")
print(f"{activity_dir = }")
print(f"{activity_base = }")
