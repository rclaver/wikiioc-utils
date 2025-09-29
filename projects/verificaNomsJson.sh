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
   echo "ruta: $directori"

   find "$directori" -type f -name "*.json" | while IFS=   read -r arxiu; do
      local dir_arxiu=$(dirname "$arxiu")
      local dir_mig=${dir_arxiu##"${dirBase}/"}
      dir_mig=${dir_mig/\//_}
      local nom_arxiu=$(basename "$arxiu")

      #echo -e "\n${CB_CYN}Ruta:${C_NONE} $dir_arxiu"
      #echo -e "${CB_CYN}Mig:${C_NONE} $dir_mig"
      #echo -e "${CB_WHT}Arxiu JSON:${C_NONE} $nom_arxiu"

      if [[ "${dir_mig}.json" == "$nom_arxiu" ]]; then
         echo "arxiu $nom_arxiu CORRECTE"
      else
         echo "Nom INCORRECTE a l'arxiu $dir_arxiu/ $nom_arxiu"
      fi
   done
}

###
# inici
#
echo -e "+-------------------------------------------------------------------------------+"
echo -e "| Verificació de la correcció dels noms de fitxer JSON al directori data/media/ |"
echo -e "+-------------------------------------------------------------------------------+"

cercar_json "$dirBase"
