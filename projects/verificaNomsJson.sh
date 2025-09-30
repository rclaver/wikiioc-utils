#!/bin/bash
###
# Verificació de la correcció dels noms de fitxer JSON al directori data/media/
###

C_NONE="\033[0m"
CB_RED="\033[1;31m"
CB_YLW="\033[1;33m"
CB_BLU="\033[1;34m"
CB_CYN="\033[1;36m"
CB_WHT="\033[1;37m"

host=`hostname`
if [[ "$host" == "wikidev" || "$host" == "dokuwiki" ]]; then
   dBase="/home/${host}"
   dirBase="${dBase}/wiki18/data/media"
else
   dirBase="/home/rafael/projectes/wiki18/data/media"
fi

function cercar_json() {
   local directori="$1"
   echo -e "\n${CB_BLU}ruta base:${CB_YLW} ${directori}${C_NONE}\n"

   find "$directori" -type f -name "*.json" | while IFS= read -r arxiu; do
      local dir_arxiu=$(dirname "$arxiu")
      local dir_mig=${dir_arxiu##"${dirBase}/"}
      dir_mig=${dir_mig//\//_}
      local nom_arxiu=$(basename "$arxiu")

      if [[ "${dir_mig}.json" != "$nom_arxiu" ]]; then
         echo -e "${CB_BLU}Nom INCORRECTE:"
         echo -e "${CB_CYN}   ruta:${C_NONE} ${dir_arxiu}/"
         echo -e "${CB_CYN}   nom desitjat:${C_NONE} ${dir_mig}.json"
         echo -e "${CB_CYN}   nom actual..:${C_NONE} ${nom_arxiu}"
      fi
   done
}

###
# inici
#
echo -e "${CB_WHT}+-------------------------------------------------------------------------------+"
echo -e "| Verificació de la correcció dels noms de fitxer JSON al directori data/media/ |"
echo -e "+-------------------------------------------------------------------------------+${C_NONE}"

cercar_json "$dirBase"
