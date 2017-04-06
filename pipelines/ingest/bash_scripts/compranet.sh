###############
# Compranet
###############
#! /bin/bash

$( chmod +x ../config/bash_password.sh )
$( sh ../config/bash_password.sh )


echo "Descarga Compranet De 2002 a 2011"
# Descargar
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/EX{2002..2011}.xlsx -P ./temp
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/LP{2002..2011}.xlsx -P ./temp

for filename in $(ls ./temp/*.xlsx)
	in2csv $filename | sed '1d' | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\|/;ta' >> ./temp/2002_2011.csv


head 2002_2011.csv | sed '1s/.*/DEPENDENCIA_ENTIDAD|NOMBRE_UC|CLAVE_UC|NUMERO_DE_PROCEDIMIENTO|TIPO_DE_PROCEDIMIENTO|TIPO_CONTRATACION|CARACTER|NUMERO_DE_CONTRATO|REFERENCIA_DE_LA_CONTRATACION| FECHA_DE_SUSCRIPCION_DE_CONTRATO|IMPORTE_MN_SIN_IVA|RAZON_SOCIAL|URL_DEL_CONTRATO/g' > compranet_2002_2011.csv
rm ./temp/EX* ./temp/LP*

echo "Descarga Compranet De 2010 a 2017"
wget --no-check-certificate  https://compranetinfo.funcionpublica.gob.mx/descargas/cnet/Contratos2010_2012.zip 
wget --no-check-certificate  https://upcp.funcionpublica.gob.mx/descargas/Contratos{2013..2017}.zip 
for f (./*.zip) unzip $f 

rm *.zip
find . -name '*.xlsx' | parallel ssconvert -T Gnumeric_stf:stf_csv {} \;
rm *.xlsx

# ToDo()
# Hace falta revisar la versión del documento antes del cambio que es del tipo 170302082128
# tenemos que guardar esta información - puede ser algo como esto:
for f (./*.csv) echo "${f%_*.*} version $f" >> metadata.txt
cat $( ls *.csv ) | sed '1d' | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\t/;ta' >> 2012_2017.csv

cat 2012_2017.csv | \
sed '1s/.*/GOBIERNO|SIGLAS|DEPENDENCIA|CLAVE_UC|NOMBRE_DE_LA_UC|RESPONSABLE|CODIGO_EXPEDIENTE|TITULO_EXPEDIENTE|PLANTILLA_EXPEDIENTE|NUMERO_PROCEDIMIENTO|EXP_F_FALLO|PROC_F_PUBLICACION|FECHA_APERTURA_PROPOSICIONES|CARACTER|TIPO_CONTRATACION|TIPO_PROCEDIMIENTO|FORMA_PROCEDIMIENTO|CODIGO_CONTRATO|TITULO_CONTRATO|FECHA_INICIO|FECHA_FIN|IMPORTE_CONTRATO|MONEDA|ESTATUS_CONTRATO|ARCHIVADO|CONVENIO_MODIFICATORIO|RAMO|CLAVE_PROGRAMA|APORTACION_FEDERAL|FECHA_CELEBRACION|CONTRATO_MARCO|IDENTIFICADOR_CM|COMPRA_CONSOLIDADA|PLURIANUAL|CLAVE_CARTERA_SHCP|ESTRATIFICACION_MUC|FOLIO_RUPC|PROVEEDOR_CONTRATISTA|ESTRATIFICACION_MPC|SIGLAS_PAIS|ESTATUS_EMPRESA|CUENTA_ADMINISTRADA_POR|C_EXTERNO|ORGANISMO|ANUNCIO/g' > compranet_2012_2017.csv
