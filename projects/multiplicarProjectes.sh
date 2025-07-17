#!/bin/bash
#
# Multiplicació de projectes a partir d'una plantilla
#

#
# Obtenir la llista de projectes a generar
# (l'arxiu que conté la llista està en format json i és el que s'utilitza per a la importació de les dades LOE a LOE24)
#
function obtenirLlista() {
   llistaProjectes=$1
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
      echo $arrProjectes
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
pt_loe='plans_de_treball'
pt_loe24='pt_fp_loe24'
dir_loe='pt_loe24_plantilla'
prj_loe='ptfploe'
prj_loe24='ptfploe24'

p_loe="${base}/@GRUP@/documents_fp/plans_de_treball/pt_loe24_plantilla/ptfploe"

p_mdpro="${base}/mdprojects/documents_fp/${pt_loe}/pt_loe24_plantilla/ptfploe"
p_pages="${base}/pages/documents_fp/${pt_loe}/pt_loe24_plantilla"
p_media="${base}/media/documents_fp/${pt_loe}/pt_loe24_plantilla"
mdpro="${base}/mdprojects/documents_fp/${pt_loe24}"

"/home/dokuwiki/wiki18/data/mdprojects/documents_fp/pt_fp_loe24/0373_ICA0B0/ptfploe24/meta.mdpr"
declare -a arrProjectes

llista=$(obtenirLlista $llistaDeProjectes)
if [[ "$llista" != "" && "$estat" != "" ]]; then
   for e in $llista; do
      for g in $grups; do
         loe=${p_loe/@GRUP@/${g}}
         if [[ "$g" = "mdprojects" ]]; then loe+="/${prj_loe}"; fi

         cp "${loe}/*" "${mdpro}/${e}/"
      done
   done
fi
