#!/bin/bash

# Rafael Claver
# 29-01-2025

C_NONE="\033[0m"
C_YLW="\033[0;36m"
CB_RED="\033[1;31m"
CB_GRN="\033[1;32m"
CB_YLW="\033[1;33m"
CB_WHT="\033[1;37m"

echo -e "${CB_WHT}+--------------------------------------------------------------------------------+"
echo -e "|      DOKUWIKI IOC: Migració d'un projecte 'projectsdev' a 'wikiiocmodel'       |"
echo -e "+--------------------------------------------------------------------------------+${C_NONE}"

if [[ "$1" == "-h" || "$1" == "-help" ]]; then
	echo -e "${CB_GRN}Ús: es demanen 2 paràmetres:"
	echo -e "\t${CB_YLW}nom_del_projecte (de projectsdev) a migrar"
	echo -e "\truta_a_la_dokuwiki${C_NONE}"
	exit 1
fi

# paràmetres per defecte
projecte=$1
ruta=$2
: ${projecte:=ptprjce}
: ${ruta:=/home/rafael/projectes/wiki18}
r_origen=${ruta}/lib/plugins/projectsdev/projects/${projecte}
r_desti=${ruta}/lib/plugins/wikiiocmodel/projects
r_desti_p=${r_desti}/${projecte}

function VerificaDirectoris() {
   if [ ! -d $r_origen ]; then
      echo -e "${CB_RED}No he tobat el directori origen ${CB_YLW}$r_origen${C_NONE}"
      return 1
   fi

   # verifica l'existència del directori de destí. Si existeix, aborta.
   if [[ -d $r_desti_p ]]; then
      echo -e "${CB_RED}El projecte ${CB_YLW}${projecte} ${CB_RED}ja existeix a ${CB_YLW}'wikiiocmodel'${C_NONE}"
      return 1
   fi
   return 0
}

function MouDirectori() {
   echo -e "${C_YLW}Movent el directori ${r_origen}"
   echo -e "${C_YLW}                  a ${r_desti_p}${C_NONE}"
   mv $r_origen $r_desti_p
}

function CercaISubstitueix() {
   arxiu=$r_desti_p/$1
   cerca=$2
   subs=$3
   echo -e "${C_YLW}Procès de cerca i substitució, a tots el fitxers, de la cadena: ${cerca} per ${subs}${C_NONE}"
   grep -lrE "$cerca" $arxiu | xargs sed -Ei -e "s/$cerca/$subs/g"
}


# ------------
# princpal
# ------------
VerificaDirectoris
[ $? == 1 ] && exit 1
MouDirectori
CercaISubstitueix "*" "plugin_projectsdev_projects_${projecte}" "plugin_wikiiocmodel_projects_${projecte}"
CercaISubstitueix "*" "('WIKI_IOC_MODEL',\s*DOKU_PLUGIN\s*\.\s*\")(projectsdev)" "\1wikiiocmodel"
echo -e "Fi del procès."
