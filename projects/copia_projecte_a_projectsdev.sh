#!/bin/bash

# Rafael Claver
# 29-01-2025

C_NONE="\033[0m"
C_YLW="\033[0;33m"
CB_RED="\033[1;31m"
CB_GRN="\033[1;32m"
CB_YLW="\033[1;33m"
CB_WHT="\033[1;37m"

echo -e "${CB_WHT}+-----------------------------------------------------------------------------------+"
echo -e "|      DOKUWIKI IOC: Còpia un projecte 'wikiiocmodel' existent a 'projectsdev'      |"
echo -e "+-----------------------------------------------------------------------------------+${C_NONE}"

if [[ "$1" == "-h" || "$1" == "-help" ]]; then
	echo -e "${CB_GRN}Ús: es demanen 3 paràmetres:"
	echo -e "\t${CB_YLW}nom_del_projecte origen"
	echo -e "\tnom_del_projecte destí"
	echo -e "\truta_a_la_dokuwiki${C_NONE}"
	exit 1
fi

# paràmetres per defecte
p_origen=$1
p_desti=$2
ruta=$3
: ${p_origen:=sintesi}
: ${p_desti:=ptprjce}
: ${ruta:=/home/rafael/projectes/wiki18}
r_origen=${ruta}/lib/plugins/wikiiocmodel/projects/${p_origen}
r_desti=${ruta}/lib/plugins/projectsdev/projects
r_desti_p=${r_desti}/${p_desti}

function VerificaDirectoris() {
   if [ ! -d $r_origen ]; then
      echo -e "${CB_RED}No he tobat el directori origen ${CB_YLW}$r_origen${C_NONE}"
      return 1
   fi

   # verifica l'existència del directori de destí. Si existeix, aborta.
   if [[ -d $r_desti_p ]]; then
      echo -e "${CB_RED}El projecte ${CB_YLW}${p_desti} ${CB_RED}ja existeix a ${CB_YLW}'projectsdev'${C_NONE}"
      return 1
   fi
   return 0
}

function CopiaDirectori() {
   echo -e "${C_YLW}Copiant el directori origen: ${p_origen} a destí: ${p_desti}${C_NONE}"
   cp -r $r_origen $r_desti
   mv $r_desti/$p_origen $r_desti_p

}

function EliminaPlantillesIUpgraders() {
   echo -e "${C_YLW}Eliminant arxius: ${r_desti_p}/upgrader/upgrader_[0-9]*.php${C_NONE}"
   rm ${r_desti_p}/upgrader/upgrader_[0-9]*.php
   echo -e "${C_YLW}Eliminant arxius: ${r_desti_p}/metadata/plantilles/continguts.txt.v[0-9]*${C_NONE}"
   rm ${r_desti_p}/metadata/plantilles/continguts.txt.v[0-9]*
}

function CercaISubstitueix() {
   arxiu=$r_desti_p/$1
   cerca=$2
   subs=$3
   echo -e "${C_YLW}Procès de cerca i substitució, a tots el fitxers, de la cadena: ${cerca} per ${subs}${C_NONE}"
   grep -lrE "$cerca" $arxiu | xargs sed -Ei -e "s/$cerca/$subs/g"
}

function RenameModelFiles() {
   echo -e "${C_YLW}Canvi de nom dels fitxers: ${p_origen}DokuModelManager.php i ${p_origen}ProjectModel.php${C_NONE}"
   echo -e "${C_YLW}                        a: ${p_desti}DokuModelManager.php i ${p_desti}ProjectModel.php${C_NONE}"
   mv $r_desti_p/${p_origen}DokuModelManager.php $r_desti_p/${p_desti}DokuModelManager.php
   mv $r_desti_p/datamodel/${p_origen}ProjectModel.php $r_desti_p/datamodel/${p_desti}ProjectModel.php
}

# ------------
# princpal
# ------------
VerificaDirectoris
[ $? == 1 ] && exit 1
CopiaDirectori
EliminaPlantillesIUpgraders
CercaISubstitueix "*" $p_origen $p_desti
CercaISubstitueix "*" "plugin_wikiiocmodel_projects_${p_desti}" "plugin_projectsdev_projects_${p_desti}"
CercaISubstitueix "*" "('WIKI_IOC_MODEL',\s*DOKU_PLUGIN\s*\.\s*\")(wikiiocmodel)" "\1projectsdev"
RenameModelFiles
echo -e "Fi del procès."
