#!/bin/bash

echo -e "--------------------------------------"
echo -e " Inici de l'enviament a ftp"
echo -e "--------------------------------------"

SERVIDOR=134.0.10.152
REMOTE_DIR=/tmp
if [ $1o != o ]; then
    SERVIDOR=$1
    BASEDIR=$2
fi

time ftp $SERVIDOR <<EOF
pasv
user sobrelar
cd $REMOTE_DIR
binary
lcd /home/wikicheck/bin/
put MicrosoftSQLfullenu.iso
bye
EOF
echo -e "--------------------------------------"
