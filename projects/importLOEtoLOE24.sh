#!/bin/bash

# Importació de dades des d'un projecte PT LOE a un projecte PT LOE24

# Taula de equivalències (original=destí)
taulaEquiv=('nsProgramacio=nsProgramacio'
            'nouCurr=nouCurr'
            'pesPAFnouCurr=pesPAFnouCurr'
            'semestre=semestre'
            'tipusBlocModul=tipusBlocModul'
            'cicle=cicle'
            'modulId=modulId'
            'modul=modul'
            'durada=durada'
            'duradaCicle=duradaCicle'
            'professors=professors'
            'coordinador=coordinador'
            'urlMaterialDidactic=urlMaterialDidactic'
            'dedicacio=dedicacio'
            'requerimentsMatricula=requerimentsMatricula'
            'descripcio=descripcio'
            'itinerarisRecomanats=itinerarisRecomanats'
            'taulaDadesUF=taulaDadesUn'
            'taulaDadesUnitats=taulaUnitatRAs'
            'einesAprenentatge=einesAprenentatge'
            'resultatsAprenentatge=resultatsAprenentatge'
            'activitatsAprenentatge=activitatsAprenentatge'
            'avaluacioInicial=avaluacioInicial'
            'calendari=calendari'
            'datesAC=datesAC'
            'hiHaSolucioPerAC=hiHaSolucioPerAC'
            'datesEAF=datesEAF'
            'treballEquipEAF=treballEquipEAF'
            'hiHaSolucioPerEAF=hiHaSolucioPerEAF'
            'hiHaEnunciatRecuperacioPerEAF=hiHaEnunciatRecuperacioPerEAF'
            'hiHaRecuperacioPerJT=hiHaRecuperacioPerJT'
            'datesJT=datesJT'
            'notaMinimaAC=notaMinimaAC'
            'notaMinimaEAF=notaMinimaEAF'
            'notaMinimaJT=notaMinimaJT'
            'dataPaf11=dataPaf11'
            'dataPaf12=dataPaf12'
            'dataPaf21=dataPaf21'
            'dataPaf22=dataPaf22'
            'dataQualificacioPaf1=dataQualificacioPaf1'
            'dataQualificacioPaf2=dataQualificacioPaf2'
            'notaMinimaPAF=notaMinimaPAF'
            'dadesQualificacioUFs=dadesQualificacioUns'
            'duradaPAF=duradaPAF'
            'dadesExtres=dadesExtres'
            'plantilla=plantilla'
            'autor=autor'
            'responsable=responsable'
            'supervisor=supervisor'
            'fitxercontinguts=fitxercontinguts'
            'moodleCourseId=moodleCourseId'
            'dataFromMix=dataFromMix'
)
itinerariRecomanats=('m\u00f2dul'
                     'itinerariRecomanatS1'
                     'itinerariRecomanatS2'
)
dadesExtres=('nom'
             'tipus'
             'valor'
             'parametres'
)
datesAC=('id'
         'unitat'
         'enunciat'
         'lliurament'
         'hiHaSolucio'
         'solució'
         'qualificació'
)
datesEAF=('id'
          'unitat'
          'enunciat'
          'lliurament'
          'hiHaSolucio'
          'solució'
          'qualificació'
          'hiHaEnunciatRecuperacio'
          'enunciat recuperació'
          'lliurament recuperació'
          'solució recuperació'
          'qualificació recuperació'
)
datesJT=('id'
         'inscripció'
         'llista provisional'
         'llista definitiva'
         'data JT'
         'qualificació'
         'hiHaRecuperacio'
         'inscripció recuperació'
         'llista provisional recuperació'
         'llista definitiva recuperació'
         'data JT recuperació'
         'qualificació recuperació'
)
calendari=('unitat'
           'període'
           'tipus període'
           'descripció període'
           'hores'
           'inici'
           'final'
)
einesAprenentatge=('tipus'
                   'eina'
                   'opcionalitat'
                   'puntuable'
)
itinerarisRecomanats=('mòdul'
                      'itinerariRecomanatS1'
                      'itinerariRecomanatS2'
)
resultatsAprenentatge=('id'
                       'descripcio'
)
activitatsAprenentatge=('unitat'
                        'període'
                        'eina'
                        'descripció'
)

# canvi de nom
taulaDadesUF=('bloc'
              'unitat formativa'
              'nom'
              'ordreImparticio'
              'hores'
              'ponderació'
)
taulaDadesUn=('bloc'
              'unitat'
              'nom'
              'ordreImparticio'
              'hores'
              'ponderació'
)
taulaDadesUnitats=('unitat formativa'
                   'unitat'
                   'nom'
                   'hores'
)
taulaUnitatRAs=('unitat'
                'RA'
)
dadesQualificacioUFs=('unitat formativa'
                      'tipus qualificació'
                      'descripció qualificació'
                      'abreviació qualificació'
                      'ponderació'
)
dadesQualificacioUns=('unitat'
                      'tipus qualificació'
                      'descripció qualificació'
                      'abreviació qualificació'
                      'ponderació'
)

# Variables globals
C_NONE="\033[0m"
CB_YLW="\033[1;33m"

declare -a arrayOrigen
jsonFinal="{"main":{"
jsonParcial=""


# llegeix l'arxiu mdpr, fragmenta la cadena json obtinguda truncant amb ","
# i guarda els elements en format array a 'arrayOrigen'
function processarArxiuDades() {
   local arxiuJson=~/projectes/wiki18/data/mdprojects/docs/loe_1/ptfploe/meta.mdpr
   local contingut=$(cat $arxiuJson)
   dadesJson=${contingut##\{\"main\":\{}  #elimina, des del principi, la part major que coincideixi amb el patró
   dadesJson=${dadesJson%\}\}}            #elimina, des del final, la part menor que coincideixi amb el patró
   IFS=',' read -r -a arrayOrigen <<< "$dadesJson"    #obté un array fent split amb el caracter ","
}


# Cerca a la Taula d'equivalències 'taulaEquiv' la parella que conté
# la clau origen sol·licitada i retorna la parella associada
function cercaEquiv() {
   local origen=${1//\"}   #elimina totes les cometes '"'
   for e in "${taulaEquiv[@]}"; do
      if [[ $e =~ $origen ]]; then
         desti=${e##*=}  # extreu la part posterior al signe "="
         break
      fi
   done
   echo $desti
}

# afegeix un nou element a la cadena de sortida 'jsonFinal' prèvia transformació de l'origen en destí
function processaJsonFinal() {
   local cadena="$1"
   local e1=${cadena//:*}  # extreu la part anterior al signe ":"
   local e2=${cadena##*:}  # extreu la part posterior al signe ":"
   local trans=$(cercaEquiv $e1)
   jsonFinal+="$trans":"$e2",
}

# afegeix un nou element a la cadena 'jsonParcial' prèvia transformació de l'origen en destí
function processaJsonParcial() {
   local cadena="$1"
   local e1=${cadena//:*}  # extreu la part anterior al signe ":"
   local e2=${cadena##*:}  # extreu la part posterior al signe ":"
   local trans=$(cercaEquiv $e1)
   jsonParcial+="$trans":"$e2",
}

function buscaParelles() {
   local restaArray="$1"
   local cadenaComp
   local valor
   local iComp=0  #indicador de 'valor' compost (conté sub-elements json)
   local claudat=0  #indicador de nivell de sub-element json (nombre de claudàtors oberts)

   for e in "${arrayOrigen[@]}"; do
      valor=${e##*:}  # extreu la part posterior al signe ":"
      # la part 'valor' és una cadena simple sense sub-elements json
      if [[ $iComp == 0 ]]; then
         if [[ $valor == '"[]"' ]]; then
            #restaArray="${restaArray[@]/$e}" # elimina l'element $e de la còpia de l'array original "restaArray"
            #simple+=("${e// /\\ }")          # escapa tots els espais ja que, si no, son delimitadors de elements de l'array
            processaJsonFinal "$e"
         elif [[ ! $e =~ "[" ]]; then
            processaJsonFinal "$e"
            #simple+=("${e// /\\ }")
         else
            iComp=1
            cadenaComp+="$e"
         fi
      else
         #la part 'valor' és part d'una cadena composta (conté sub-elements json)
         cadenaComp+="$e"
         echo -e "${CB_YLW}\tcadenaComp=${cadenaComp}${C_NONE}"
         if [[ $e =~ "[" ]]; then
            let claudat++
            echo -e "${CB_YLW}\t\tclaud=${claud}${C_NONE}"
         elif [[ $e =~ "]" ]]; then
            let claudat--
            if [[ $claudat == 0 ]]; then
               processaJsonParcial "$cadenaComp"
               iComp=0
            fi
         fi
      fi
   done
}


# ---------------------
# INICI
# ---------------------
echo -e "${CB_YLW}+------------------------------------------------------------------------+"
echo -e "|  Importació de dades des d'un projecte PT LOE a un projecte PT LOE24  |"
echo -e "+------------------------------------------------------------------------+${C_NONE}"

processarArxiuDades
   #echo -e "${CB_YLW}dadesJson${C_NONE}\n${dadesJson}\n"
   echo -e "${CB_YLW}arrayOrigen${C_NONE}"
   for e in "${arrayOrigen[@]}"; do
      echo -e "\t$e"
   done
   echo

# processa l'array
buscaParelles $arrayOrigen

echo "........."
echo "RESULTATS"
echo "........."
#for e in "${simple[@]}"; do
#   echo $e
#done
echo "........."
jsonFinal+="}}"
echo -e "${CB_YLW}--- jsonFinal ---${C_NONE}\n$jsonFinal"
echo "........."

echo "------------------------------"
#read -p "Procès finalitzat. Prem Retorn"
