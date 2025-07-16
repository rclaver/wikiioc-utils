#!/bin/bash

# Importació de dades des d'un projecte PT LOE a un projecte PT LOE24

# Taula de equivalències (original=destí)
taulaEquiv=('taulaDadesUF:taulaDadesUn'
            'taulaDadesUnitats:taulaUnitatRAs'
            'dadesQualificacioUFs:dadesQualificacioUns'
)
#nota: els elements d'una taula es separen amb espai
#substituim els espais dels noms dels elements per @
taulaDadesUF=('bloc:bloc'
              'unitat@formativa:unitat'
              'nom:nom'
              'ordreImparticio:ordreImparticio'
              'hores:hores'
              'ponderaci\\u00f3:ponderaci\\u00f3"'
)
taulaDadesUnitats=('unitat@formativa:unitat'
                   'unitat:RA'
                   'nom:'
                   'hores:"'
)
dadesQualificacioUFs=('unitat@formativa:unitat'
                      'tipus@qualificació:tipus@qualificació'
                      'descripció@qualificació:descripció@qualificació'
                      'abreviació@qualificació:abreviació@qualificació'
                      'ponderaci\\u00f3:ponderaci\\u00f3"'
)

#
# Variables globals
LANG=C.UTF-8
C_NONE="\033[0m"
CB_YLW="\033[1;33m"

declare -a arrayOrigen
jsonFinal="{\"main\":{"

#
# llegeix l'arxiu mdpr, fragmenta la cadena json obtinguda truncant amb ","
# i guarda els elements en format array a 'arrayOrigen'
#
function llegeixArxiu() {
   local arxiu=$1
   local contingut=$(cat $arxiu)
   dades=${contingut##\{\"main\":\{}  	#elimina, des del principi, la part major que coincideixi amb el patró
   dades=${dades%\}\}}            	  	#elimina, des del final, la part menor que coincideixi amb el patró
   IFS=',' read -r -a arrayOrigen <<< "$dades"    #obté un array fent split amb el caracter ","
}


#
# Obté la part value de la parella key:value
#
function getValue() {
   local key=${1//\"}   #elimina totes les cometes '"'
   echo ${key#*:}       # extreu la part posterior al primer signe ":"
}

#
# Cerca a la Taula d'equivalències 'taulaEquiv' la parella que conté
# la clau origen sol·licitada i retorna la parella associada
#
function cercaTaulaEquiv() {
   local e
   local origen=${1//\"}   #elimina totes les cometes '"'
   local desti=$origen
   for e in "${taulaEquiv[@]}"; do
      if [[ "${e}" =~ "${origen}:" ]]; then
         desti=${e#*:}  #extreu la part posterior al primer signe ":"
         break
      fi
   done
   echo $desti
}

#
# Cerca a la taula d'equivalències especificada la parella que conté
# la clau origen sol·licitada i retorna la parella associada
#
function cercaEquiv() {
   local e taula
   local nomTaula=$1
   local korigen=$2
   local desti=""
   eval "taula=\$(echo" \${$nomTaula[@]} ")" #captura l'estructura de l'array indicat amb el nom 'nomTaula'
   read -r -a taula <<< "$taula"             #converteix la cadena $taula en un array fent split amb el caracter " "

   for e in "${taula[@]}"; do
      e=${e/@/ }   #subtitueix el caracter @ per espai
      if [[ "${e}" =~ "${korigen}:" ]]; then
         desti=${e#*:}  #extreu la part posterior al primer signe ":"
         break
      fi
   done
   echo ${desti//\"}  #elimina les cometes
}

#
# afegeix un nou element a la cadena de sortida 'jsonFinal' prèvia transformació de l'origen en destí
#
function processaJsonFinal() {
   local cadena="$1"
   local e1=${cadena//:*}  # extreu la part anterior al signe ":"
   local e2=${cadena#*:}   # extreu la part posterior al primer signe ":"
   local trans=$(cercaTaulaEquiv $e1)
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
   local transKey=$(cercaTaulaEquiv $keyOrigen)   # key principal transformada en la seva equivalent

   if [[ "$transKey" == "" ]]; then
      echo # no s'ha d'incloure aquest element
   elif [[ "$keyOrigen" == "$transKey" ]]; then
      #incorpora l'element sense canvis al jsonFinal
      jsonFinal+="${json},"   #afegeix coma de separació del següent element
   else
      local jArray elem jElem e k v i parcial
      local novaKV="\"${transKey}\":\"["

      local valueOrigen=${json#*:}            #extreu el valor (la part posterior al primer signe ":")
      valueOrigen=${valueOrigen//[\[\]]}      #elimina tots els claudàtors
      valueOrigen=${valueOrigen##\"}          #elimina les cometes '"' inicials
      valueOrigen=${valueOrigen%%\"}          #elimina les cometes '"' finals
      valueOrigen=${valueOrigen//\},\{/\};\{} #canvia "," per ";" com a separador de sub-elements json "{......}"

      echo -e "${CB_YLW}processaJsonParcial()${C_NONE} json=${json}"
      echo -e "\t${CB_YLW}keyOrigen:${C_NONE}${keyOrigen}\n\t${CB_YLW}valueOrigen:${C_NONE}${valueOrigen}\n"

      # Converteix la part $valueOrigen en un array i processa els elements
      IFS=';' read -r -a jArray <<< "$valueOrigen"    #crea un array fent split amb el caracter ";"

      for e in "${jArray[@]}"; do
         echo -e "${CB_YLW}jArray[n] = ${C_NONE}${e}"
      done
      echo -e "\n"

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
            echo -e "\t${CB_YLW}k=${C_NONE}${k} - ${CB_YLW}v=${C_NONE}${v}"

            kt=$(cercaEquiv ${keyOrigen} "${k}")  #transforma la key en la seva correponent a partir de la taula denominada $keyOrigen
            echo -e "\t${CB_YLW}kt=${C_NONE}${kt}\n"

            #afegeix el valor -per posició a l'array- a la key transformada (sempre i quan existeixi)
            if [[ "${kt}]" != "" ]]; then
               parcial+="\\\"${kt}\\\":${v},"
            fi
            (( i++ ))
         done
         parcial=${parcial%,}    #elimina la coma final
         novaKV+="${parcial}},"
         echo -e "\t\t${CB_YLW}novaKV=${C_NONE}${novaKV}\n"
      done
      novaKV=${novaKV%,}            #elimina la coma final
      jsonFinal+="${novaKV}]\","    #afegeix claudàtor de tancament, cometes finals i coma
   fi
}

#
# Procés principal: tractament de tots els elements de l'arrayOrigen
#
function proces() {
   local cadenaComp e valor
   local iComp=0  #indicador de 'valor' compost (conté sub-elements json)
   local claud=0  #indicador de nivell de sub-element json (nombre de claudàtors oberts)

   for e in "${arrayOrigen[@]}"; do
      valor=${e#*:}  # extreu la part posterior al primer signe ":"
      # la part 'valor' és una cadena simple sense sub-elements json
      if [[ $iComp == 0 ]]; then
         if [[ $valor == '"[]"' ]]; then
            processaJsonFinal "$e"
         elif [[ ! $e =~ "[" ]]; then
            processaJsonFinal "$e"
         else
            iComp=1
            let claud++
            cadenaComp="${e},"
         fi
      else
         #la part 'valor' és part d'una cadena composta (conté sub-elements json)
         cadenaComp+="${e},"
         echo -e "P ${CB_YLW}e=${C_NONE}${e}"
         echo -e "P ${CB_YLW}cadenaComp=${C_NONE}${cadenaComp}"
         if [[ $e =~ "[" ]]; then
            let claud++
         elif [[ $e =~ "]" ]]; then
            let claud--
            if [[ $claud == 0 ]]; then
               echo -e "P ${CB_YLW}claud = ${claud}${C_NONE}\n"
               cadenaComp=${cadenaComp%,}   #elimina la coma final
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

llegeixArxiu "meta.mdpr"
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
jsonFinal=${jsonFinal%,}   #elimina la coma final
jsonFinal+="}}"
echo -e "${CB_YLW}--- jsonFinal ---${C_NONE}\n$jsonFinal"

echo "------------------------------"
#read -p "Procès finalitzat. Prem Retorn"
