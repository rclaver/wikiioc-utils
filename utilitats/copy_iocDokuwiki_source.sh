#!/bin/bash
#
# Copia los directorios fuente de la IOC-dokuwiki al repositorio de wikicheck
#
C_NONE="\033[0m"
C_CYN="\033[0;36m"
C_WHT="\033[0;37m"
CB_CYN="\033[1;36m"
CB_WHT="\033[1;37m"

function Copia() {
	origen=/home/rafael/nb-projectes/$1/
	destino=wikicheck@wikicheck.ioc.cat::2112:/home/wikicheck/repositori2015/$1/
	echo -e "${C_CYN}origen  = $origen"
	echo -e "destino = $destino${CB_CYN}"

	read -p "¿Quieres copiar el directorio '$1' al repositorio de wikicheck (s/N)? " -n1 r
	resp=${r:-N} #asignación del valor por defecto
	echo -e ${C_NONE}
	if [[ $resp == [Ss] ]]; then
		echo -e "${C_WHT}- copiando $origen"
		echo -e         "        en $destino"
		#sshpass -p XB4bwaFX rsync -u -zvqa --rsh=ssh $origen $destino
		rsync -u -zvqa $origen $destino
	fi
}

echo -e "${CB_WHT}---------------------------------------------------------------------------"
echo -e "Copia los directorios fuente de la IOC-dokuwiki al repositorio de wikicheck"
echo -e "---------------------------------------------------------------------------\n"
Copia "ace-builds"
Copia "dokuwiki_30"
Copia "iocjslib"

#Notas para rsync
# -c : skip based on checksum, not mod-time & size
# -u : skip files that are newer on the receiver
# --size-only : skip files that match in size
# -e, --rsh=COMMAND : specify the remote shell to use
# -a : archive mode; equals -rlptgoD (no -H,-A,-X)
# -l : copy symlinks as symlinks
# -p : preserve permissions
# -o : preserve owner (super-user only)
# -g : preserve group
# -t : preserve modification times
# -r : recurse into directories
# -q : suppress non-error messages
# -v : increase verbosity
# -z : compress file data during the transfer
# -n : perform a trial run with no changes made

