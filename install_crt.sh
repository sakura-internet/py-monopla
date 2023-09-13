#!/bin/bash

CRT_FILE=Sakura_Iot_SIPF_Root_CA_1.crt
CRT_DIR=/usr/share/ca-certificates
CRT_SUBDIR=SakuraInternet

mkdir -p ${CRT_DIR}/${CRT_SUBDIR}

cp ${CRT_FILE} ${CRT_DIR}/${CRT_SUBDIR}/ 

echo ${CRT_SUBDIR}/${CRT_FILE} >> /etc/ca-certificates.conf
update-ca-certificates

ls -l /etc/ssl/certs/ | grep ${CRT_SUBDIR}
