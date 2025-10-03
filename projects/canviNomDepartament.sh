#!/bin/bash
#
# Canvi de nom del Departament
#
C_NONE="\033[0m"
C_YLW="\033[0;33m"
CB_RED="\033[1;31m"
CB_GRN="\033[1;32m"
CB_YLW="\033[1;33m"
CB_WHT="\033[1;37m"

cerca_basica="Departament"
patro_cerca="(Departament (d&#39;Educació|d'Educació|d’Ensenyament|d'Ensenyament))( i Formació Professional)?"
substitucio="Departament d'Educació i Formació Professional"

#sed -Ei -e "s/(Departament (d&#39;Educació|d'Educació|d’Ensenyament|d'Ensenyament))(?(?= i Formació)( i Formació Professional)|())/Departament d'Educació i Formació Professional/g"

host=`hostname`
if [[ "$host" == "wikidev" || "$host" == "dokuwiki" ]]; then
   dBase="/home/${host}"
   dirBase1="${dBase}/wiki18/lib/plugins"
   dirBase2="${dBase}/wiki18/data/pages/plantilles"
else
   dBase="/home/rafael/projectes"
   dirBase1="${dBase}/wiki18/lib/plugins"
   dirBase2="${dBase}/wiki18/data/pages/plantilles"
fi

function cerca() {
   local directori="$1"
   echo -e "\n${CB_BLU}ruta base:${CB_YLW} ${directori}${C_NONE}"
   find "$directori" -type f | while IFS= read -r arxius; do
      arxiu=$(grep --color=auto -HI "Departament" ${arxius})
      if [[ -n $arxiu ]]; then
         echo -e "${CB_RED}cerca:${C_NONE} $arxiu"
      fi
   done
}

# #####
# inici
#
echo -e "${CB_WHT}+------------------------------+"
echo -e "| Canvi de nom del Departament |"
echo -e "+------------------------------+${C_NONE}"

if [ ! -f canviNomDepartament ]; then
   echo -e "${CB_YLW}Processant els arxius del directori ${CB_WHT}lib/plugins${C_NONE}"
   grep -lrE "$cerca_basica" "${dirBase1}/" | xargs sed -Ei -e "s/$patro_cerca/$substitucio/g"
   echo "$(date +"[%d/%m/%Y - %H:%M]"): El canvi de nom del Departament a lib/plugins ja s'ha realitzar. No es pot tornar a repetir.'" > canviNomDepartament
   echo -e "\n${CB_YLW}Processant els arxius del directori ${CB_WHT}data/pages/plantilles${C_NONE}"
   grep -lrE "$cerca_basica" "${dirBase2}/" | xargs sed -Ei -e "s/$patro_cerca/$substitucio/g"
   echo "$(date +"[%d/%m/%Y - %H:%M]"): El canvi de nom del Departament a data/pages/plantilles ja s'ha realitzar. No es pot tornar a repetir.'" >> canviNomDepartament
else
   echo -e "\n${CB_YLW}Mostra els arxius del directori ${CB_WHT}lib/plugins${C_NONE}"
   cerca "$dirBase1"
   echo -e "\n${CB_YLW}Mostra els arxius del directori ${CB_WHT}data/pages/plantilles${C_NONE}"
   cerca "$dirBase2"
fi
