#!/bin/bash
#
# Canvi de nom del Departament
#

search=("Departament d&#39;Educació",
        "Departament d'Educació",
        "Departament d’Ensenyament",
        "Departament d'Ensenyament"
)
replace="Departament d'Educació i Formació Professional"

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


function canvi() {
   local directori="$1"
   echo -e "\n${CB_BLU}ruta base:${CB_YLW} ${directori}${C_NONE}\n"
   find "$directori" -type f | while IFS= read -r arxiu; do
      r=$(grep -HIo ${arxiu})
      echo $r
   done
}

# inici
#
echo -e "${CB_WHT}+---------------------+"
echo -e "| Canvi de nom del Departament |"
echo -e "+------------------------------+${C_NONE}"

canvi "$dirBase1"
read -p "prem return per a la 2a tanda" -r
canvi "$dirBase2"
