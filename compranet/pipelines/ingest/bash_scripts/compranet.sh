#! /bin/bash
#### Description: Ingestion de Compranet 2010 a 2016
###############

#wget
#unzip
#parallel
#ssconvert

echo "Descarga Compranet De $1 "

# Create temporal directory
mkdir ../../data/$1

wget --no-check-certificate  https://upcp.funcionpublica.gob.mx/descargas/Contratos$1.zip -P \
	../../data/$1

for f in $( ls ../../data/$1/*.zip ); do unzip "$f" -d ../../data/compranet_2010_2016; done; 
rm ../../data/$1/*.zip

find ../../data/compranet_2010_2016 -name '*.xlsx' | parallel ssconvert -D ../../data/compranet_2010_2016/ -T Gnumeric_stf:stf_csv {} \; \
 && rm ../../data/compranet_2010_2016/*.xlsx

cat $( find ../../data/compranet_2010_2016 -name '*.csv' ) | sed '1d' | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\t/;ta' | \
	sed 's/\t/|/g'  >> ../../data/compranet_2010_2016/2010_2016.csv

cat ../../data/compranet_2010_2016/2010_2016.csv | sed '1s/.*/GOBIERNO|SIGLAS|DEPENDENCIA|CLAVE_UC|NOMBRE_DE_LA_UC|RESPONSABLE|CODIGO_EXPEDIENTE|TITULO_EXPEDIENTE|PLANTILLA_EXPEDIENTE|NUMERO_PROCEDIMIENTO|EXP_F_FALLO|PROC_F_PUBLICACION|FECHA_APERTURA_PROPOSICIONES|CARACTER|TIPO_CONTRATACION|TIPO_PROCEDIMIENTO|FORMA_PROCEDIMIENTO|CODIGO_CONTRATO|TITULO_CONTRATO|FECHA_INICIO|FECHA_FIN|IMPORTE_CONTRATO|MONEDA|ESTATUS_CONTRATO|ARCHIVADO|CONVENIO_MODIFICATORIO|RAMO|CLAVE_PROGRAMA|APORTACION_FEDERAL|FECHA_CELEBRACION|CONTRATO_MARCO|IDENTIFICADOR_CM|COMPRA_CONSOLIDADA|PLURIANUAL|CLAVE_CARTERA_SHCP|ESTRATIFICACION_MUC|FOLIO_RUPC|PROVEEDOR_CONTRATISTA|ESTRATIFICACION_MPC|SIGLAS_PAIS|ESTATUS_EMPRESA|CUENTA_ADMINISTRADA_POR|C_EXTERNO|ORGANISMO|ANUNCIO/g' > ../../data/compranet_2010_2016.csv

# deletes the temp directory
rm -rf ../../data/compranet_2010_2016
echo "Deleted temp working directory"

