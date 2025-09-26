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

function recorregut() {
   dir_actual=$1
   cd $dir_actual
   echo -e "dir_actual: ${dir_actual}"

   for arxiu in $(ls -1 --group-directories-first); do
      ruta="${dir_actual}/${arxiu}"
      if [ -d $arxiu ]; then
         echo -e "\n${CB_BLU}RUTA: ${CB_YLW}${ruta}${C_NONE}"
         recorregut $arxiu
         read i
         cd ..
      else
         echo -e "${CB_CYN}arxiu: ${CB_WHT}$dir_actual/ $arxiu ${C_NONE}"
         ext=${arxiu##*.}
         if [[ "$ext" == "json" ]]; then
            echo -e "arxiu: ${arxiu}"
         fi
      fi
   done
}

###
# inici
#
recorregut $dirBase
