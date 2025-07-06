#!/bin/bash

echo -e "--------------------------------------"
echo -e " Inici de l'enviament a ftp-ioc"
echo -e "--------------------------------------"
SERVIDOR=materials@ftp-ioc.xtec.cat
BASEDIR=/html/FP/Recursos/_TMP/
if [ $1o != o ]; then
    SERVIDOR=$1
    BASEDIR=$2
fi

time sftp $SERVIDOR <<EOF
progress
lcd /home/wikicheck/bin
lls -l *.iso
progress
cd $BASEDIR
put MicrosoftSQLfullenu.iso
bye
EOF
echo -e "--------------------------------------"
