#!/bin/bash
#
# @autor: Rafael Claver
# @descipció: Multiplicació de projectes a partir d'una plantilla
#

#
# Obtenir la llista de projectes a generar
# (l'arxiu que conté la llista està en format json i és el que s'utilitza per a la importació de les dades LOE a LOE24)
#
function obtenirLlista() {
   llistaProjectes=$1
   declare -a arrProjectes
   if [ -f $llistaProjectes ]; then

      llp=$(cat $llistaProjectes)
      llp=${llp#\{}   #elimina, des del principi, la part que coincideixi amb el patró
      llp=${llp%\}}   #elimina, des del final, la part menor que coincideixi amb el patró

      for parella in $llp; do
         parella=${parella//\"}  #elimina cometes
         proj=${parella#*:}      #part posterior a :
         proj=${proj%,}          #elimina la coma final
         arrProjectes+=($proj)
      done
      echo ${arrProjectes[@]}
   else
      estat="No he trobar el fitxer \'${llistaProjectes}\' que conté la llista de projectes"
   fi
}

# ---------------------
# INICI
# ---------------------
echo -e "${CB_YLW}+-------------------------------------------------------+"
echo -e "|  Multiplicació de projectes a partir d'una plantilla  |"
echo -e "+-------------------------------------------------------+${C_NONE}"

llistaDeProjectes="llistaPTLOE.txt"
base="/home/dokuwiki/wiki18/data"

grups=('mdprojects' 'pages' 'media')
prj='ptfploe24'            #tipus de projecte LOE24
pt='pt_fp_loe24'           #directori dels plans de treball LOE24
pdir='pt_loe24_plantilla'  #directori de la plantilla LOE24

plantilla="${base}/@GRUP@/documents_fp/${pt}/${pdir}"

llista=$(obtenirLlista $llistaDeProjectes)

if [[ "$estat" = "" ]]; then
   echo -e "llista = ${llista}\n"

   for elem in $llista; do
      elem=${elem%${prj}\/meta.mdpr}   #elimina la part final que inclou el tipus de projecte 'ptfploe24/meta.mdpr'

      for g in ${grups[@]}; do
         #canvia el directori de grup
         desti=${elem/mdprojects/${g}}
         plant=${plantilla/@GRUP@/${g}}

         if [[ "$g" = "mdprojects" ]]; then
            plant+="/${prj}"  #afegeix el directori de classe de projecte
         else
            plant+="/*"       #indica que només s'ha de copiar el contingut del directori'
         fi

         if [ -f $plant -o -d $plant ]; then
            echo -e "-plant=${plant}\n-desti=${desti}\n"
            mkdir -p $desti
            cp -r $plant $desti
         fi
      done
   done
else
   echo -e "${estat}\n"
fi
