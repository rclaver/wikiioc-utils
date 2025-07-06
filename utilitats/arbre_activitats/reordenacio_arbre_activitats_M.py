#!/usr/bin/python
# -*- coding: UTF8 -*-
import os, sys, socket, shutil, json

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
print(CB_CYN+"=============================================================================")
print(CB_CYN+" Reorganització dels fitxers exportats dels projectes activityutil MAJÚSCULES")
print(CB_CYN+"============================================================================="+C_NONE)

# Valors per defecte
LOG = "../bin/links_sftp_activitats.txt"
PREFIX="documents_fp_docencia_activitats_"
if (socket.gethostname() == "LM19"):
	MDPROJECTS="/home/rafael/Vídeos/mdprojects/activitats"
	ACTIVITY_DIR="/home/rafael/Vídeos/ActivityUtil"
else:
	MDPROJECTS="/home/wikidev/wiki18/data/mdprojects/documents_fp/docencia/activitats/"
	ACTIVITY_DIR="../ActivityUtil.restes"		#/html/FP/Recursos/ActivityUtil

SIMULACIO = "S"
ACTUAL_PROJECT = ""

def sintaxi():
	print(CB_WHT+"Sintaxi:")
	print(CB_WHT+"   -f | --file "+U_WHT+"file"+C_WHT+": fitxer amb els paràmetres de configuració")
	print(CB_GRN+"       format del fitxer: "+CB_CYN+"key=\"value\" "+C_WHT+"(1 per línia)")
	print(CB_GRN+"           valors de key: "+CB_CYN+"[mdprojects, activity_dir, prefix, simulació]")
	print(CB_YLW+"           el valor de activity_dir ha de començar per "+CB_WHT+"\"./\"")
	print(CB_WHT+"   -m | --mdprojects   "+U_WHT+"valor"+C_WHT+": ruta absoluta de l'arbre de projectes a tractar")
	print(CB_WHT+"   -d | --activity_dir "+U_WHT+"valor"+C_WHT+": ruta relativa de l'arbre de directoris FTP")
	print(CB_WHT+"   -x | --prefix       "+U_WHT+"valor"+C_WHT+": part del nom de directori corresponent als projectes")
	print(CB_WHT+"   -s | --simulació    "+U_WHT+"valor"+C_WHT+": 'S' indica Simulació, 'E' indica Execució" + C_NONE)
	return

def actualParams():
	global MDPROJECTS, ACTIVITY_DIR, PREFIX, SIMULACIO
	print(CB_RED+"\nEls paràmetres actuals son:"+C_NONE)
	print("  >> mdprojects   = " + CB_YLW + MDPROJECTS + C_NONE)
	print("  >> activity_dir = " + CB_YLW + ACTIVITY_DIR + C_NONE)
	print("  >> prefix       = " + CB_YLW + PREFIX + C_NONE)
	print("  >> simulació    = " + CB_YLW + SIMULACIO + C_NONE)
	r = raw_input("\nVols continuar? s/N: ")
	if (r.upper() != "S"): exit()

	r = raw_input("\nVols modificar els paràmetres? s/N: ")
	if (r.upper() == "S"):
		r = raw_input(CB_WHT+"  mdprojects   " +CB_CYN + "(" + MDPROJECTS + ") = " +C_NONE)
		if (r): MDPROJECTS = r
		r = raw_input(CB_WHT+"  activity_dir " +CB_CYN + "(" + ACTIVITY_DIR + ") = " +C_NONE)
		if (r): ACTIVITY_DIR = r
		r = raw_input(CB_WHT+"  prefix       " +CB_CYN + "(" + PREFIX + ") = " +C_NONE)
		if (r): PREFIX = r
		r = raw_input(CB_WHT+"  simulació    " +CB_CYN + "(" + SIMULACIO + ") = " +C_NONE)
		if (r): SIMULACIO = r

		actualParams()

# Tratamiento de los argumentos de la línea de comandos
arg = sys.argv[1:]
while arg:
	if (arg[0]=="-f" or arg[0]=="--file"):
		if (os.path.exists(arg[1]+".py")):
			params = __import__(arg[1])
			MDPROJECTS = params.mdprojects
			ACTIVITY_DIR = params.activity_dir
			PREFIX = params.prefix
			break
		else:
			exit()
	elif (arg[0]=="-m" or arg[0]=="--mdprojects"):
		MDPROJECTS = arg[1]
	elif (arg[0]=="-d" or arg[0]=="--activity_dir"):
		ACTIVITY_DIR = arg[1]
	elif (arg[0]=="-x" or arg[0]=="--prefix"):
		PREFIX = arg[1]
	elif (arg[0]=="-s" or arg[0]=="--simulació"):
		SIMULACIO = arg[1]
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

# Busca en el directorio ACTIVITY_DIR los directorios que coincidan con el nombre de la página de proyecto
# Entonces crea un directorio de nombre project y mueve los directorios
# encontrados a este nuevo directorio
# A continuación crea unlaces simbólicos en ACTIVITY_DIR que apuntan a los
# directorios anteriormente movidos
def creaEstructura(page_project):

	x = 0
	for fitxer in listFiles:
		if (fitxer > page_project):
#			print("   -pr- "+ACTUAL_PROJECT)
#			print("   -pg- "+page_project)
#			print("      x "+fitxer)
			break

		if (fitxer == page_project):
			print("   -pr- "+CB_GRN+ACTUAL_PROJECT+C_NONE)
			print("   -pg- "+CB_GRN+fitxer+C_NONE)
			origin = ACTIVITY_DIR+"/"+fitxer
			new_dir = ACTIVITY_DIR+"/"+PREFIX+ACTUAL_PROJECT+"/"
			destination = (new_dir+fitxer).replace(" ","")
			destination_low = (new_dir+fitxer.lower()).replace(" ","")

			tmp_dir = ACTIVITY_DIR+"/../OA/"+PREFIX+ACTUAL_PROJECT+"/"
			destination_tmp = (tmp_dir+fitxer).replace(" ","")
			destination_tmp_low = (tmp_dir+fitxer.lower()).replace(" ","")

			print(CB_CYN+"    origen:["+CB_GRN+origin+CB_CYN+"]"+C_NONE)
			print(CB_CYN+"     destí:["+CB_GRN+destination_low+CB_CYN+"]"+C_NONE)

			f = open(LOG, "a")

			# Crea, si no existeix, el directori de projecte
			if (not os.path.exists(ACTIVITY_DIR+"/../OA/")):
				os.mkdir(ACTIVITY_DIR+"/../OA/")
			if (not os.path.exists(tmp_dir)):
				os.mkdir(tmp_dir)
			if (not os.path.exists(new_dir)):
				f.write('mkdir ' + new_dir + '\n')
				print(CB_RED+"  creat el directori: "+CB_WHT+new_dir+C_NONE)

			# if no existeix el directori 'destination' mou el directori 'origin' al directori de projecte
			# en cas contrari, elimina el directori 'origin' ja que un altre procés ja havia creat una nova versió
			if (not os.path.exists(destination_low)):
				print(CB_CYN+"    movent origen ["+CB_GRN+origin+CB_CYN+"]"+C_NONE)
				print(CB_CYN+"          a destí ["+CB_GRN+destination_low+CB_CYN+"]"+C_NONE)
				if (SIMULACIO == "E"):
					os.rename(origin, destination_tmp_low)
				f.write('rename ' + origin + ' ' + destination_low + '\n')
			elif (os.path.exists(destination)):
				print(CB_RED+"    eliminant destination ["+CB_GRN+destination+CB_CYN+"]"+C_NONE)
				#if (SIMULACIO == "E"):
					#shutil.rmtree(origin, ignore_errors=True)
				x += 1
				f.write("rename " + destination + " 000_" + str(x) + "\n")

			print(CB_CYN+"    creant link de destí ["+CB_GRN+destination_low+CB_CYN+"]"+C_NONE)
			print(CB_CYN+"               en origen ["+CB_GRN+origin+CB_CYN+"]"+C_NONE)
			#if (SIMULACIO == "E"):
				#os.symlink(destination, origin)
			f.write("ln -s " + destination_low + ' ' + origin + '\n')
			f.write("ln -s " + destination_low + ' ' + origin.lower() + '\n')
			f.close()

	return


# Volta el directori mdprojects cercant projectes.
# Les rutes -transformades- dels projectes son la base per a la
# reorganització dels fitxers exportats dels projectes activityutil
def voltarProjectes(pr_dir):
	global ACTUAL_PROJECT

	def transformDir(dir, glue, **params):
		spl = dir.split("/")
		# valors per defecte
		common_path = MDPROJECTS
		add_prefix = ""
		for key in params:
			if (key == 'common_path'): common_path = params[key]
			if (key == 'add_prefix'): add_prefix = params[key]

		#eliminamos del array spl los nmdp primeros elementos que corresponden a la ruta common_path
		#y, si no hay PREFIX, los 2 elementos finales: el nombre del directorio actual y el del fichero _wikiIocSystem_.mdpr
		if (add_prefix == ""):
			nmdp = len([c for c in common_path if c=="/"]) + 1
			spl = spl[nmdp:-2]

		ret = add_prefix + glue.join(spl)
		return ret

	listProjects = os.listdir(pr_dir)
	listProjects.sort()

	for file in listProjects:
		actual = pr_dir+"/"+file
		if (os.path.isdir(actual)):
			voltarProjectes(actual)
		else:
			if (file == "_wikiIocSystem_.mdpr"):
				f = open(pr_dir+"/meta.mdpr", "r")
				meta = f.read()
				meta = json.loads(meta)
				try:
					documents = meta["main"]["documents"]
					documents = json.loads(documents)

					ACTUAL_PROJECT = transformDir(actual, "_")
					project_dir = transformDir(actual, "/")
					print(C_NONE+"------------------------------------------------------")
					print(C_NONE+"projecte: "+ACTUAL_PROJECT+" | ruta: "+project_dir)
					print(C_NONE+"------------------------------------------------------")

					for doc in documents:
						doc_actual = project_dir+"/"+doc["nom"]
						#print (CB_RED+"  doc actual: "+C_NONE+doc_actual)
						doc_project = transformDir(doc_actual, "_", add_prefix=PREFIX)
						#print (CB_RED+"  doc project: "+C_NONE+doc_project)
						creaEstructura(doc_project)
				except:
					continue
	return

# ----
# main
# ----
voltarProjectes(MDPROJECTS)
print("=== FI ===")

