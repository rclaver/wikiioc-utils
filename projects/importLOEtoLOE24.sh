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
itinerariRecomanats=('m\\u00f2dul'
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
              'unitat\\u0020formativa'
              'nom'
              'ordreImparticio'
              'hores'
              'ponderaci\\u00f3'
)
taulaDadesUn=('bloc'
              'unitat'
              'nom'
              'ordreImparticio'
              'hores'
              'ponderaci\\u00f3'
)
taulaDadesUnitats=('unitat\\u0020formativa'
                   'unitat'
                   'nom'
                   'hores'
)
taulaUnitatRAs=('unitat'
                'RA'
)
dadesQualificacioUFs=('unitat\\u0020formativa'
                      'tipus\\u0020qualificació'
                      'descripció\\u0020qualificació'
                      'abreviació\\u0020qualificació'
                      'ponderaci\\u00f3'
)
dadesQualificacioUns=('unitat'
                      'tipus\\u0020qualificació'
                      'descripció\\u0020qualificació'
                      'abreviació\\u0020qualificació'
                      'ponderaci\\u00f3'
)

#
# Variables globals
LANG=C.UTF-8

C_NONE="\033[0m"
CB_YLW="\033[1;33m"

declare -a arrayOrigen
jsonFinal="{"main":{"


#
# llegeix l'arxiu mdpr, fragmenta la cadena json obtinguda truncant amb ","
# i guarda els elements en format array a 'arrayOrigen'
#
function processarArxiuDades() {
   local arxiuJson=~/projectes/wiki18/data/mdprojects/docs/loe_1/ptfploe/meta.mdpr
   local contingut=$(cat $arxiuJson)
   dadesJson=${contingut##\{\"main\":\{}  #elimina, des del principi, la part major que coincideixi amb el patró
   dadesJson=${dadesJson%\}\}}            #elimina, des del final, la part menor que coincideixi amb el patró
   IFS=',' read -r -a arrayOrigen <<< "$dadesJson"    #obté un array fent split amb el caracter ","
}


#
# Cerca a la Taula d'equivalències 'taulaEquiv' la parella que conté
# la clau origen sol·licitada i retorna la parella associada
#
function cercaEquiv() {
   local e
   local origen=${1//\"}   #elimina totes les cometes '"'
   for e in "${taulaEquiv[@]}"; do
      if [[ "${e}" =~ "${origen}=" ]]; then
         desti=${e##*=}  # extreu la part posterior a l'últim signe "="
         break
      fi
   done
   echo $desti
}

#
# afegeix un nou element a la cadena de sortida 'jsonFinal' prèvia transformació de l'origen en destí
#
function processaJsonFinal() {
   local cadena="$1"
   local e1=${cadena//:*}  # extreu la part anterior al signe ":"
   local e2=${cadena##*:}  # extreu la part posterior a l'últim signe ":"
   local trans=$(cercaEquiv $e1)
   jsonFinal+="\"$trans\"":"$e2",
}

#
# Tractament d'un json parcial.
# es tracta d'una cadena del tipus '"key_principal":"[{"key1":"value1"}{"key2":"value2"}{...}]"'
#
function processaJsonParcial() {
   local json=$1
   local keyOrigen=${json//:*}               # extreu la key principal del json (la part anterior al signe ":")
   keyOrigen=${keyOrigen//\"}                # elimina les cometes
   local transKey=$(cercaEquiv $keyOrigen)   # key principal transformada en la seva equivalent

   if [[ "$keyOrigen" == "$transKey" ]]; then
      #incorpora l'element sense canvis al jsonFinal
      jsonFinal+="${json},"   #afegeix coma de separació del següent element
   else
      local arrTrans jArray elem jElem e k v i parcial
      local novaKV="\"${transKey}\":\"["

      eval "arrTrans=\$(echo" \${$transKey[@]} ")" #captura l'estructura de l'array indicat a 'transKey'
      read -r -a arrTrans <<< "$arrTrans"          #crea un array fent split amb el caracter " "

      local valueOrigen=${json#*:}           #extreu el valor (la part posterior al primer signe ":")
      valueOrigen=${valueOrigen//[\[\]]}     #elimina tots els claudàtors
      valueOrigen=${valueOrigen##\"}         #elimina les cometes '"' inicials
      valueOrigen=${valueOrigen%%\"}         #elimina les cometes '"' finals
      valueOrigen=${valueOrigen//\}\{/\},\{} #afegeix "," com a separador de sub-elements json "{......}"

      echo -e "${CB_YLW}processaJsonParcial()${C_NONE} json=${json}\n"
      echo -e "\t${CB_YLW}keyOrigen:${C_NONE}${keyOrigen}\n\t${CB_YLW}valueOrigen:${C_NONE}${valueOrigen}"

      # Converteix la part $valueOrigen en un array i processa els elements
      IFS=',' read -r -a jArray <<< "$valueOrigen"    #crea un array fent split amb el caracter ","

      for elem in "${jArray[@]}"; do
         jElem=${elem//\\\"\\\"/\\\",\\\"}      #afegeix "," com a separador de sub-elements json \"......\":\"......\"
         jElem=$(echo "$jElem" | sed -E 's/(:[0-9]+)\\"/\1,\\"/g')  #afegeix "," com a separador de sub-elements json \"......\":99
         echo -e "\t${CB_YLW}jElem=${C_NONE}${jElem}"

         # Transforma la parella key:value a la versió destí, és a dir, genera una nova key:value amb la key corresponent al destí
         IFS=',' read -r -a aElem <<< "$jElem"  #crea un array fent split amb el caracter ","

         parcial="{"
         i=0
         for e in "${aElem[@]}"; do
            e=${e//[\{\}]}     #elimina totes les claus "{}" (inicial i final)
            echo -e "\t${CB_YLW}e=${C_NONE}${e}"

            k=${e//:*}         #key original de la parella
            k=${k//\\\"}       #elimina totes les barres davant cometes (inicial i final)
            v=${e#*:}          #value de la parella
            echo -e "\t${CB_YLW}k=${C_NONE}${k} -- ${CB_YLW}v=${C_NONE}${v}"

            echo -e "\t\t arrTrans ----\t${CB_YLW}arrTrans[$i]=${C_NONE}${arrTrans[$i]}"
            #afegeix el valor -per posició a l'array- a la key transformada (sempre i quan existeixi)
            if [[ "arrTrans[$i]" != "" ]]; then
               parcial+="\\\"${arrTrans[$i]}\\\":${v},"
            fi
            (( i++ ))
         done
         parcial=${parcial%,}    #elimina la coma final
         novaKV+="${parcial}},"
         echo -e "\t\t${CB_YLW}novaKV=${C_NONE}${novaKV}"
      done
      novaKV=${novaKV%,}            #elimina la coma final
      jsonFinal+="${novaKV}]\","    #afegeix claudàtor de tancament, cometes finals i coma
   fi
}

#
# Procés principal: tractament de tots els elements de l'arrayOrigen
#
function proces() {
   local cadenaComp valor e
   local iComp=0  #indicador de 'valor' compost (conté sub-elements json)
   local claud=0  #indicador de nivell de sub-element json (nombre de claudàtors oberts)

   for e in "${arrayOrigen[@]}"; do
      valor=${e##*:}  # extreu la part posterior al signe ":"
      # la part 'valor' és una cadena simple sense sub-elements json
      if [[ $iComp == 0 ]]; then
         if [[ $valor == '"[]"' ]]; then
            processaJsonFinal "$e"
         elif [[ ! $e =~ "[" ]]; then
            processaJsonFinal "$e"
         else
            iComp=1
            let claud++
            cadenaComp="$e"
         fi
      else
         #la part 'valor' és part d'una cadena composta (conté sub-elements json)
         cadenaComp+="$e"
         echo -e "P ${CB_YLW}e=${C_NONE}${e}"
         echo -e "P ${CB_YLW}cadenaComp=${C_NONE}${cadenaComp}"
         if [[ $e =~ "[" ]]; then
            let claud++
            echo -e "P ${CB_YLW}\tclaud1=${claud}\n$C_NONE"
         elif [[ $e =~ "]" ]]; then
            let claud--
            echo -e "P ${CB_YLW}\tclaud0=${claud}\n$C_NONE"
            if [[ $claud == 0 ]]; then
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
proces $arrayOrigen

echo "~~~~~~~~"
echo "RESULTAT"
echo "~~~~~~~~"
jsonFinal+="}}"
echo -e "${CB_YLW}--- jsonFinal ---${C_NONE}\n$jsonFinal"

echo "------------------------------"
#read -p "Procès finalitzat. Prem Retorn"
