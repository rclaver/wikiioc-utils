#!/usr/bin/python
# -*- coding: UTF8 -*-
import os, sys, socket, shutil

C_NONE="\033[0m"
C_CYN="\033[0;36m"  #normal
C_WHT="\033[0;37m"
CB_RED="\033[1;31m" #bold
CB_YLW="\033[1;33m"
CB_WHT="\033[1;37m"
CB_CYN="\033[1;36m"
CB_GRN="\033[1;32m"
U_WHT=C_NONE+"\033[4;37m"   # underline

print(sys.version_info)
print("hostname: "+socket.gethostname())
print(CB_CYN+"==================================================================")
print(CB_CYN+" Generació de rm pel directori ActivityUtil_nou de ftp-ioc")
print(CB_CYN+"=================================================================="+C_NONE)

# Valors per defecte
if (socket.gethostname() == "LM19"):
	ACTIVITY_DIR="/home/rafael/Vídeos/ActivityUtil"
else:
	ACTIVITY_DIR="../ActivityUtil"		#/html/FP/Recursos/ActivityUtil

LOG = "../bin/rm_sftp_activitats.txt"

def sintaxi():
	print(CB_WHT+"Sintaxi:")
	print(CB_WHT+"   -d | --activity_dir "+U_WHT+"valor"+C_WHT+": ruta relativa de l'arbre de directoris FTP")
	return

def actualParams():
	global ACTIVITY_DIR
	print(CB_RED+"\nEls paràmetres actuals son:"+C_NONE)
	print("  >> activity_dir = " + CB_YLW + ACTIVITY_DIR + C_NONE)
	r = raw_input("\nVols continuar? s/N: ")
	if (r.upper() != "S"): exit()

	r = raw_input("\nVols modificar els paràmetres? s/N: ")
	if (r.upper() == "S"):
		r = raw_input(CB_WHT+"  activity_dir " +CB_CYN + "(" + ACTIVITY_DIR + ") = " +C_NONE)
		if (r): ACTIVITY_DIR = r

		actualParams()

# Tratamiento de los argumentos de la línea de comandos
arg = sys.argv[1:]
while arg:
	if (arg[0]=="-d" or arg[0]=="--activity_dir"):
		ACTIVITY_DIR = arg[1]
	elif (arg[0]=="-h" or arg[0]=="--help"):
		sintaxi()
		exit()
	arg = arg[2:]

if (len(arg) == 0):
	sintaxi()
	actualParams()

print(C_NONE)

# Establecer el directorio ACTIVITY_DIR como directorio actual
os.chdir(ACTIVITY_DIR)
ACTIVITY_DIR = "."

try:
	os.unlink(LOG)
except:
	None

listFiles = os.listdir(ACTIVITY_DIR)
listFiles.sort()

# Busca en el directorio ACTIVITY_DIR todos los directorios
# A continuación añade una sentencia rm para los directorios hallados
def voltarDirectori():
	global LOG

	# Voltar el directori per obtenir tots els seus elements que han de ser eliminats per SFTP
	def voltaLinks(f, ldir):
		linklist = os.listdir(ldir)
		linklist.sort()

		for lfile in linklist:
			actual = ldir+"/"+lfile
			if (os.path.isdir(actual)):
				voltaLinks(f, actual)
				f.write("rmdir " + actual + "\n")
			else:
				f.write("rm " + actual + "\n")

		return

	for file in listFiles:
		print("   -pg- "+CB_GRN+file+C_NONE)
		f = open(LOG, "a")
		voltaLinks(f, file)
		f.write("rmdir " + file + "\n")
		f.close()

	return

# ----
# main
# ----
voltarDirectori()
print("=== FI ===")

